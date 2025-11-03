from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User


users_bp = Blueprint("users", __name__)


def get_courses_details(course_ids):
    if not course_ids:
        return []

    from app.models import Course

    courses = Course.query.filter(Course.id.in_(course_ids)).all()
    return [course.to_dict() for course in courses]


def get_blogs_details(blog_ids):
    if not blog_ids:
        return []

    from app.models import Blog

    blogs = Blog.query.filter(Blog.id.in_(blog_ids)).all()
    return [blog.to_dict() for blog in blogs]


@users_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@users_bp.route("/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    username = data.get("username")
    email = data.get("email")

    if not username or not email:
        return jsonify({"error": "Username and email are required"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    user = User(
        username=username,
        email=email,
        owned_courses=[],
        favourite_courses=[],
        saved_blogs=[],
    )
    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@users_bp.route("/users/<int:user_id>/profile", methods=["GET"])
def get_user_profile(user_id):
    """Get user profile with expanded course and blog details"""
    user = User.query.get_or_404(user_id)

    user_data = user.to_dict()
    user_data["owned_courses"] = get_courses_details(user.owned_courses or [])
    user_data["favourite_courses"] = get_courses_details(user.favourite_courses or [])
    user_data["saved_blogs"] = get_blogs_details(user.saved_blogs or [])

    return jsonify(user_data)


@users_bp.route("/users/<int:user_id>/owned-courses", methods=["GET"])
def get_owned_courses(user_id):
    user = User.query.get_or_404(user_id)
    expand = request.args.get("expand", "false").lower() == "true"

    if expand:
        courses = get_courses_details(user.owned_courses or [])
        return jsonify({"user_id": user.id, "owned_courses": courses}), 200

    return jsonify({"user_id": user.id, "owned_courses": user.owned_courses or []}), 200


@users_bp.route("/users/<int:user_id>/owned-courses", methods=["POST"])
def add_owned_course(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    course_id = data.get("course_id")
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    if user.owned_courses is None:
        user.owned_courses = []

    if course_id not in user.owned_courses:
        user.owned_courses.append(course_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "Course already owned"}), 200


@users_bp.route(
    "/users/<int:user_id>/owned-courses/<int:course_id>", methods=["DELETE"]
)
def remove_owned_course(user_id, course_id):
    user = User.query.get_or_404(user_id)

    if user.owned_courses and course_id in user.owned_courses:
        user.owned_courses.remove(course_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Course not found in owned courses"}), 404


@users_bp.route("/users/<int:user_id>/favourite-courses", methods=["GET"])
def get_favourite_courses(user_id):
    user = User.query.get_or_404(user_id)
    expand = request.args.get("expand", "false").lower() == "true"

    if expand:
        courses = get_courses_details(user.favourite_courses or [])
        return jsonify({"user_id": user.id, "favourite_courses": courses}), 200

    return jsonify(
        {"user_id": user.id, "favourite_courses": user.favourite_courses or []}
    ), 200


@users_bp.route("/users/<int:user_id>/favourite-courses", methods=["POST"])
def add_favourite_course(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    course_id = data.get("course_id")
    if not course_id:
        return jsonify({"error": "course_id is required"}), 400

    if user.favourite_courses is None:
        user.favourite_courses = []

    if course_id not in user.favourite_courses:
        user.favourite_courses.append(course_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "Course already in favourites"}), 200


@users_bp.route(
    "/users/<int:user_id>/favourite-courses/<int:course_id>", methods=["DELETE"]
)
def remove_favourite_course(user_id, course_id):
    user = User.query.get_or_404(user_id)

    if user.favourite_courses and course_id in user.favourite_courses:
        user.favourite_courses.remove(course_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Course not found in favourites"}), 404


@users_bp.route("/users/<int:user_id>/saved-blogs", methods=["GET"])
def get_saved_blogs(user_id):
    user = User.query.get_or_404(user_id)
    expand = request.args.get("expand", "false").lower() == "true"

    if expand:
        blogs = get_blogs_details(user.saved_blogs or [])
        return jsonify({"user_id": user.id, "saved_blogs": blogs}), 200

    return jsonify({"user_id": user.id, "saved_blogs": user.saved_blogs or []}), 200


@users_bp.route("/users/<int:user_id>/saved-blogs", methods=["POST"])
def add_saved_blog(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    blog_id = data.get("blog_id")
    if not blog_id:
        return jsonify({"error": "blog_id is required"}), 400

    if user.saved_blogs is None:
        user.saved_blogs = []

    if blog_id not in user.saved_blogs:
        user.saved_blogs.append(blog_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"message": "Blog already saved"}), 200


@users_bp.route("/users/<int:user_id>/saved-blogs/<int:blog_id>", methods=["DELETE"])
def remove_saved_blog(user_id, blog_id):
    user = User.query.get_or_404(user_id)

    if user.saved_blogs and blog_id in user.saved_blogs:
        user.saved_blogs.remove(blog_id)
        db.session.commit()
        return jsonify(user.to_dict()), 200

    return jsonify({"error": "Blog not found in saved blogs"}), 404


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    expand = request.args.get("expand", "false").lower() == "true"

    if expand:
        user_data = user.to_dict()
        user_data["owned_courses"] = get_courses_details(user.owned_courses or [])
        user_data["favourite_courses"] = get_courses_details(
            user.favourite_courses or []
        )
        user_data["saved_blogs"] = get_blogs_details(user.saved_blogs or [])
        return jsonify(user_data)

    return jsonify(user.to_dict())


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user_id != 1:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": f"User {user.username} deleted successfully."}), 200
    return jsonify({"error": "Cannot delete user with ID 1"}), 403
