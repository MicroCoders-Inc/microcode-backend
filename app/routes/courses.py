from flask import Blueprint, jsonify, request, send_file
from sqlalchemy.exc import IntegrityError
from app.models import Course, User
from app.database import db
from app.auth_middleware import token_required
from app.pdf_generator import generate_course_pdf

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return jsonify(
        {
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )

@courses_bp.route("/courses/<int:course_id>", methods=["GET"])
def get_course_by_id(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        return jsonify(course.to_dict()), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred while retrieving the course: {str(e)}"}), 500


@courses_bp.route("/courses/<int:course_id>/download-pdf", methods=["GET"])
@token_required
def download_course_pdf(current_user_id, course_id):
    """
    Download course as PDF - only accessible to course owners
    Accepts optional 'theme' query parameter: 'light' (default) or 'dark'
    """
    try:
        # Get theme from query parameter, default to 'light'
        theme = request.args.get('theme', 'light')
        if theme not in ['light', 'dark']:
            theme = 'light'

        # Get the course
        course = Course.query.get_or_404(course_id)

        # Get the current user
        user = User.query.get(current_user_id)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Check if user owns the course
        owned_courses = user.owned_courses or []
        if course_id not in owned_courses:
            return jsonify({"error": "You must own this course to download it as PDF"}), 403

        # Generate PDF with theme
        pdf_file = generate_course_pdf(course.to_dict(), theme=theme)

        # Create a safe filename with theme indicator
        safe_filename = f"{course.name.replace(' ', '_')}_{theme}.pdf"

        # Send the PDF file
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=safe_filename
        )

    except Exception as e:
        return jsonify({"error": f"An error occurred while generating the PDF: {str(e)}"}), 500


@courses_bp.route("/courses", methods=["POST"])
def create_course():
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Validate required fields
    required_fields = ["name", "price", "discount", "topic", "level", "description"]
    for field in required_fields:
        if field not in data or data[field] is None:
            return jsonify({"error": f"Missing required field: {field}"}), 400

    try:
        # Create new course
        course = Course(
            name=data["name"],
            price=data["price"],
            discount=data["discount"],
            topic=data["topic"],
            level=data["level"],
            description=data["description"],
            tags=data.get("tags", []),
            summary=data.get("summary"),
            image_url=data.get("image_url"),
            image_alt=data.get("image_alt"),
        )

        db.session.add(course)
        db.session.commit()

        return jsonify({"message": "Course created successfully", "course": course.to_dict()}), 201

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "course_name" in error_msg or "UNIQUE constraint" in error_msg:
            return jsonify({"error": f"A course with the name '{data.get('name')}' already exists"}), 409
        return jsonify({"error": f"Database integrity error: {error_msg}"}), 400

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@courses_bp.route("/courses/<int:course_id>", methods=["PUT"])
def update_course(course_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        course = Course.query.get_or_404(course_id)

        # Update fields if provided
        if "name" in data:
            course.name = data["name"]
        if "price" in data:
            course.price = data["price"]
        if "discount" in data:
            course.discount = data["discount"]
        if "topic" in data:
            course.topic = data["topic"]
        if "level" in data:
            course.level = data["level"]
        if "description" in data:
            course.description = data["description"]
        if "tags" in data:
            course.tags = data["tags"]
        if "summary" in data:
            course.summary = data["summary"]
        if "content" in data:
            course.content = data["content"]
        if "image_url" in data:
            course.image_url = data["image_url"]
        if "image_alt" in data:
            course.image_alt = data["image_alt"]

        db.session.commit()

        return jsonify({"message": "Course updated successfully", "course": course.to_dict()}), 200

    except IntegrityError as e:
        db.session.rollback()
        error_msg = str(e.orig)
        if "course_name" in error_msg or "UNIQUE constraint" in error_msg:
            return jsonify({"error": f"A course with the name '{data.get('name')}' already exists"}), 409
        return jsonify({"error": f"Database integrity error: {error_msg}"}), 400

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while updating the course: {str(e)}"}), 500


@courses_bp.route("/courses/<int:course_id>", methods=["DELETE"])
def delete_course(course_id):
    try:
        course = Course.query.get_or_404(course_id)
        course_name = course.name

        db.session.delete(course)
        db.session.commit()

        return jsonify({"message": f"Course '{course_name}' deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred while deleting the course: {str(e)}"}), 500


@courses_bp.route("/courses/frontend", methods=["GET"])
def get_frontend_courses():
    courses = Course.query.filter_by(topic="frontend").all()
    return jsonify(
        {
            "topic": "frontend",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/backend", methods=["GET"])
def get_backend_courses():
    courses = Course.query.filter_by(topic="backend").all()
    return jsonify(
        {
            "topic": "backend",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/database", methods=["GET"])
def get_database_courses():
    courses = Course.query.filter_by(topic="database").all()
    return jsonify(
        {
            "topic": "database",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/git", methods=["GET"])
def get_git_courses():
    courses = Course.query.filter_by(topic="git").all()
    return jsonify(
        {
            "topic": "git",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )
