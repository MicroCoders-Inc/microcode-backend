"""
Purchase routes for course purchasing functionality
"""

from datetime import datetime
from flask import Blueprint, request, jsonify
from sqlalchemy.orm import joinedload
from app.database import db
from app.models import User, Course, Purchase
from app.auth_middleware import token_required

purchases_bp = Blueprint('purchases', __name__)


@purchases_bp.route('/purchase', methods=['POST'])
@token_required
def purchase_courses(current_user_id):
    """
    Purchase one or more courses

    Request body:
    {
        "course_ids": [1, 2, 3]  # List of course IDs to purchase
    }

    Returns:
    {
        "message": "Purchase successful",
        "purchases": [...],  # List of purchase records
        "invoice_numbers": [...],  # List of invoice numbers
        "user": {...}  # Updated user object with owned_courses
    }
    """
    try:
        data = request.get_json()

        if not data or 'course_ids' not in data:
            return jsonify({'error': 'course_ids is required'}), 400

        course_ids = data['course_ids']

        if not isinstance(course_ids, list) or len(course_ids) == 0:
            return jsonify({'error': 'course_ids must be a non-empty list'}), 400

        # Get the user
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({'error': 'User not found'}), 404

        # Initialize owned_courses if None
        if user.owned_courses is None:
            user.owned_courses = []

        purchases = []
        invoice_numbers = []

        for course_id in course_ids:
            # Check if course exists
            course = Course.query.get(course_id)
            if not course:
                return jsonify({'error': f'Course with ID {course_id} not found'}), 404

            # Check if user already owns this course
            if course_id in user.owned_courses:
                return jsonify({'error': f'You already own course: {course.name}'}), 400

            # Calculate final price (price - discount)
            price_paid = float(course.price)
            discount_applied = float(course.discount) if course.discount else 0.0
            final_price = max(0, price_paid - discount_applied)

            # Generate invoice number
            invoice_number = Purchase.generate_invoice_number()

            # Create purchase record
            purchase = Purchase(
                user_id=current_user_id,
                course_id=course_id,
                price_paid=price_paid,
                discount_applied=discount_applied,
                final_price=final_price,
                invoice_number=invoice_number,
                purchase_date=datetime.utcnow()
            )

            db.session.add(purchase)
            purchases.append(purchase.to_dict())
            invoice_numbers.append(invoice_number)

            # Add course to user's owned courses
            user.owned_courses.append(course_id)

        # Mark user.owned_courses as modified (needed for MutableList)
        from sqlalchemy.orm.attributes import flag_modified
        flag_modified(user, 'owned_courses')

        # Commit all changes
        db.session.commit()

        return jsonify({
            'message': 'Purchase successful',
            'purchases': purchases,
            'invoice_numbers': invoice_numbers,
            'user': user.to_dict()
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@purchases_bp.route('/purchases', methods=['GET'])
@token_required
def get_user_purchases(current_user_id):
    """
    Get all purchases for the authenticated user

    Query params:
    - expand=true: Include full course details in response

    Returns:
    {
        "count": 5,
        "purchases": [...]
    }
    """
    try:
        expand = request.args.get('expand', 'false').lower() == 'true'

        # Get all purchases for this user with eager loading to avoid N+1 queries
        query = Purchase.query.filter_by(user_id=current_user_id)

        if expand:
            # Use joinedload to fetch courses in a single query
            query = query.options(joinedload(Purchase.course))

        purchases = query.all()

        result = []
        for purchase in purchases:
            purchase_dict = purchase.to_dict()

            if expand and purchase.course:
                # Course is already loaded from joinedload
                purchase_dict['course'] = purchase.course.to_dict()

            result.append(purchase_dict)

        return jsonify({
            'count': len(result),
            'purchases': result
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@purchases_bp.route('/invoices/<invoice_number>', methods=['GET'])
def get_invoice(invoice_number):
    """
    Get invoice details by invoice number
    No authentication required - anyone with invoice number can view

    Returns:
    {
        "invoice_number": "INV-XXXXX",
        "purchase_date": "2024-01-15T10:30:00",
        "user": {...},
        "course": {...},
        "price_paid": 29.99,
        "discount_applied": 5.00,
        "final_price": 24.99
    }
    """
    try:
        purchase = Purchase.query.filter_by(invoice_number=invoice_number).first()

        if not purchase:
            return jsonify({'error': 'Invoice not found'}), 404

        # Get user and course details
        user = User.query.get(purchase.user_id)
        course = Course.query.get(purchase.course_id)

        invoice_data = purchase.to_dict()

        if user:
            invoice_data['user'] = {
                'id': user.id,
                'username': user.username,
                'email': user.email
            }

        if course:
            invoice_data['course'] = course.to_dict()

        return jsonify(invoice_data), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500
