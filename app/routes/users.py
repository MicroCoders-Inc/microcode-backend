from flask import Blueprint, jsonify, request
from app.database import db
from app.models import User

users_bp = Blueprint("users", __name__)


@users_bp.route("/users", methods=["GET"])
def get_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])


@users_bp.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())


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

    user = User(username=username, email=email)

    db.session.add(user)
    db.session.commit()

    return jsonify(user.to_dict()), 201


@users_bp.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return jsonify({"message": f"User {user.username} deleted successfully."}), 200
