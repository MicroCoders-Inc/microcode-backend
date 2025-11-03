from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Blog
from app.validation import validate_email, validate_string_field
from app.constants import MAX_BLOG_TITLE_LENGTH, MAX_BLOG_DESCRIPTION_LENGTH

blogs_bp = Blueprint("blogs", __name__)


@blogs_bp.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = Blog.query.order_by(Blog.publication_date.desc()).all()
    return jsonify([blog.to_dict() for blog in blogs])


@blogs_bp.route("/blogs", methods=["POST"])
def create_blog():
    data = request.get_json()

    # Validate title
    is_valid, error = validate_string_field(data.get("title"), "Title", MAX_BLOG_TITLE_LENGTH)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate author_name
    is_valid, error = validate_string_field(data.get("author_name"), "Author name", 100)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate email
    is_valid, error = validate_email(data.get("email"))
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate url
    is_valid, error = validate_string_field(data.get("url"), "URL", 255)
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate description
    is_valid, error = validate_string_field(data.get("description"), "Description", MAX_BLOG_DESCRIPTION_LENGTH)
    if not is_valid:
        return jsonify({"error": error}), 400

    new_blog = Blog(
        title=data.get("title"),
        author_name=data.get("author_name"),
        email=data.get("email"),
        url=data.get("url"),
        description=data.get("description"),
    )
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201
