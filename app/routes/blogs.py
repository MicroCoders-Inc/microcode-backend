from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from app.database import db
from app.models import Blog
from app.validation import validate_email, validate_string_field
from app.constants import MAX_BLOG_TITLE_LENGTH, MAX_BLOG_DESCRIPTION_LENGTH, MAX_BLOG_CONTENT_LENGTH

blogs_bp = Blueprint("blogs", __name__)


@blogs_bp.route("/blogs", methods=["GET"])
def get_blogs():
    blogs = Blog.query.order_by(Blog.publication_date.desc()).all()
    return jsonify([blog.to_dict() for blog in blogs])


@blogs_bp.route("/blogs/<int:blog_id>", methods=["GET"])
def get_blog(blog_id):
    blog = Blog.query.get_or_404(blog_id)
    return jsonify(blog.to_dict()), 200


@blogs_bp.route("/blogs", methods=["POST"])
def create_blog():
    data = request.get_json()

    # Validate title
    is_valid, error = validate_string_field(
        data.get("title"), "Title", MAX_BLOG_TITLE_LENGTH
    )
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
    is_valid, error = validate_string_field(
        data.get("description"), "Description", MAX_BLOG_DESCRIPTION_LENGTH
    )
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate content (NUEVO)
    is_valid, error = validate_string_field(
        data.get("content"), "Content", MAX_BLOG_CONTENT_LENGTH
    )
    if not is_valid:
        return jsonify({"error": error}), 400

    try:
        new_blog = Blog(
            title=data.get("title"),
            author_name=data.get("author_name"),
            email=data.get("email"),
            url=data.get("url"),
            description=data.get("description"),
            content=data.get("content"),  # NUEVO
            tags=data.get("tags", []),
            image_url=data.get("image_url"),
            image_alt=data.get("image_alt"),
        )
        db.session.add(new_blog)
        db.session.commit()
        return jsonify(
            {"message": "Blog created successfully", "blog": new_blog.to_dict()}
        ), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


@blogs_bp.route("/blogs/<int:blog_id>", methods=["PUT"])
def update_blog(blog_id):
    data = request.get_json()

    if not data:
        return jsonify({"error": "No data provided"}), 400

    try:
        blog = Blog.query.get_or_404(blog_id)

        # Validate and update fields if provided
        if "title" in data:
            is_valid, error = validate_string_field(
                data.get("title"), "Title", MAX_BLOG_TITLE_LENGTH
            )
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.title = data["title"]

        if "author_name" in data:
            is_valid, error = validate_string_field(
                data.get("author_name"), "Author name", 100
            )
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.author_name = data["author_name"]

        if "email" in data:
            is_valid, error = validate_email(data.get("email"))
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.email = data["email"]

        if "url" in data:
            is_valid, error = validate_string_field(data.get("url"), "URL", 255)
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.url = data["url"]

        if "description" in data:
            is_valid, error = validate_string_field(
                data.get("description"), "Description", MAX_BLOG_DESCRIPTION_LENGTH
            )
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.description = data["description"]

        # Validate and update content (NUEVO)
        if "content" in data:
            is_valid, error = validate_string_field(
                data.get("content"), "Content", MAX_BLOG_CONTENT_LENGTH
            )
            if not is_valid:
                return jsonify({"error": error}), 400
            blog.content = data["content"]

        if "tags" in data:
            blog.tags = data["tags"]

        if "image_url" in data:
            blog.image_url = data["image_url"]

        if "image_alt" in data:
            blog.image_alt = data["image_alt"]

        db.session.commit()

        return jsonify(
            {"message": "Blog updated successfully", "blog": blog.to_dict()}
        ), 200

    except ValueError as e:
        db.session.rollback()
        return jsonify({"error": f"Invalid value provided: {str(e)}"}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"An error occurred while updating the blog: {str(e)}"}
        ), 500


@blogs_bp.route("/blogs/<int:blog_id>", methods=["DELETE"])
def delete_blog(blog_id):
    try:
        blog = Blog.query.get_or_404(blog_id)
        blog_title = blog.title

        db.session.delete(blog)
        db.session.commit()

        return jsonify({"message": f"Blog '{blog_title}' deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify(
            {"error": f"An error occurred while deleting the blog: {str(e)}"}
        ), 500