"""
Validation utilities for user input.
"""

import re

# Constants for validation
MIN_USERNAME_LENGTH = 3
MIN_PASSWORD_LENGTH = 6
MAX_USERNAME_LENGTH = 80
MAX_EMAIL_LENGTH = 120

# Email validation regex (RFC 5322 simplified)
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')


def validate_email(email):
    """
    Validate email format using regex.

    Args:
        email: Email string to validate

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not email or not isinstance(email, str):
        return False, "Email is required"

    if len(email) > MAX_EMAIL_LENGTH:
        return False, f"Email must be less than {MAX_EMAIL_LENGTH} characters"

    if not EMAIL_REGEX.match(email):
        return False, "Invalid email format"

    return True, None


def validate_username(username):
    """
    Validate username format and length.

    Args:
        username: Username string to validate

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not username or not isinstance(username, str):
        return False, "Username is required"

    if len(username) < MIN_USERNAME_LENGTH:
        return False, f"Username must be at least {MIN_USERNAME_LENGTH} characters"

    if len(username) > MAX_USERNAME_LENGTH:
        return False, f"Username must be less than {MAX_USERNAME_LENGTH} characters"

    # Username should only contain alphanumeric, underscore, and hyphen
    if not re.match(r'^[a-zA-Z0-9_-]+$', username):
        return False, "Username can only contain letters, numbers, underscores, and hyphens"

    return True, None


def validate_password(password):
    """
    Validate password strength.

    Args:
        password: Password string to validate

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not password or not isinstance(password, str):
        return False, "Password is required"

    if len(password) < MIN_PASSWORD_LENGTH:
        return False, f"Password must be at least {MIN_PASSWORD_LENGTH} characters"

    return True, None


def validate_string_field(value, field_name, max_length, required=True):
    """
    Generic string field validation.

    Args:
        value: Value to validate
        field_name: Name of the field (for error messages)
        max_length: Maximum allowed length
        required: Whether the field is required

    Returns:
        tuple: (is_valid: bool, error_message: str|None)
    """
    if not value:
        if required:
            return False, f"{field_name} is required"
        return True, None

    if not isinstance(value, str):
        return False, f"{field_name} must be a string"

    if len(value) > max_length:
        return False, f"{field_name} must be less than {max_length} characters"

    return True, None
