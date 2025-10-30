from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Blog

blogs_bp = Blueprint("blogs", __name__)


@blogs_bp.route("/blogs", methods=["GET"])
def get_blogs():
    return jsonify({"status": "ok"})

@blogs_bp.route("/blogs", methods=["POST"])
def create_blog():
    data = request.get_json()
    new_blog = Blog(
        title=data.get("title"),
        author_name=data.get("author_name"),
        email=data.get("email"),
        url=data.get("url"),
        description=data.get("description")
    )
    db.session.add(new_blog)
    db.session.commit()
    return jsonify(new_blog.to_dict()), 201
