"""
Authentication middleware for JWT token verification.
"""

from functools import wraps
from flask import request, jsonify
import jwt
import os
from app.models import User


def verify_user_authorization(current_user_id, target_user_id, action_description="access this resource"):
    """
    Helper function to verify that the current user is authorized to perform an action
    on the target user's resource.

    Args:
        current_user_id: ID of the currently authenticated user
        target_user_id: ID of the user whose resource is being accessed
        action_description: Description of the action for error message

    Returns:
        None if authorized, or (error_dict, status_code) tuple if not authorized
    """
    if current_user_id != target_user_id:
        return jsonify({"error": f"Unauthorized: You can only {action_description}"}), 403
    return None


def _extract_and_validate_token():
    """
    Helper function to extract and validate JWT token from request headers.

    Returns:
        tuple: (user_id, error_response)
        - If successful: (user_id, None)
        - If failed: (None, (error_dict, status_code))
    """
    token = None

    # Check if Authorization header exists
    if 'Authorization' in request.headers:
        auth_header = request.headers['Authorization']
        # Expected format: "Bearer <token>"
        try:
            token = auth_header.split(" ")[1]
        except IndexError:
            return None, (jsonify({'error': 'Invalid token format. Use: Bearer <token>'}), 401)

    if not token:
        return None, (jsonify({'error': 'Authentication token is missing'}), 401)

    try:
        # Decode the token
        secret_key = os.environ.get('SECRET_KEY')
        if not secret_key:
            return None, (jsonify({'error': 'Server configuration error'}), 500)

        data = jwt.decode(token, secret_key, algorithms=["HS256"])
        current_user_id = data['user_id']
        return current_user_id, None

    except jwt.ExpiredSignatureError:
        return None, (jsonify({'error': 'Token has expired'}), 401)
    except jwt.InvalidTokenError:
        return None, (jsonify({'error': 'Invalid token'}), 401)
    except Exception:
        return None, (jsonify({'error': 'Token validation failed'}), 401)


def token_required(f):
    """
    Decorator to protect routes that require authentication.
    Validates JWT token from Authorization header and injects user_id into the route.

    Usage:
        @token_required
        def protected_route(current_user_id):
            # current_user_id is automatically injected
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_id, error = _extract_and_validate_token()
        if error:
            return error

        # Pass the user_id to the route
        return f(current_user_id, *args, **kwargs)

    return decorated


def token_optional(f):
    """
    Decorator for routes that work with or without authentication.
    If token is present and valid, injects user_id. Otherwise, injects None.

    Usage:
        @token_optional
        def maybe_protected_route(current_user_id):
            if current_user_id:
                # User is authenticated
                pass
            else:
                # User is not authenticated
                pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_id, _ = _extract_and_validate_token()
        # Ignore errors - optional auth means we accept None
        if current_user_id is None:
            current_user_id = None  # Explicit for clarity

        return f(current_user_id, *args, **kwargs)

    return decorated


def admin_required(f):
    """
    Decorator to protect routes that require admin authentication.
    Validates JWT token AND checks if user has admin role.
    Returns 403 Forbidden if user is not an admin.

    Usage:
        @admin_required
        def admin_only_route(current_user_id):
            # current_user_id is automatically injected
            # User is guaranteed to be an admin
            pass
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        current_user_id, error = _extract_and_validate_token()
        if error:
            return error

        # Check if user exists and has admin role
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        if user.role != 'admin':
            return jsonify({'error': 'Admin access required. You do not have permission to access this resource.'}), 403

        # User is authenticated and is an admin
        return f(current_user_id, *args, **kwargs)

    return decorated
