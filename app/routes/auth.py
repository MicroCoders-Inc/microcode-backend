from flask import Blueprint, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os
from app.database import db
from app.models import User

auth_bp = Blueprint("auth", __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-here")


@auth_bp.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()

    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    if not username or not email or not password:
        return jsonify({"error": "All fields are required"}), 400

    if len(username) < 3:
        return jsonify({"error": "Username must be at least 3 characters"}), 400

    if len(password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    if "@" not in email:
        return jsonify({"error": "Invalid email format"}), 400

    if User.query.filter_by(username=username).first():
        return jsonify({"error": "Username already exists"}), 409

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already exists"}), 409

    # Hash the password
    hashed_password = generate_password_hash(password)

    user = User(
        username=username,
        email=email,
        password_hash=hashed_password,
        owned_courses=[],
        favourite_courses=[],
        saved_blogs=[],
    )

    db.session.add(user)
    db.session.commit()

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({"token": token, "user": user.to_dict()}), 201


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()

    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()

    if not user or not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid email or password"}), 401

    # Generate JWT token
    token = jwt.encode(
        {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7),
        },
        SECRET_KEY,
        algorithm="HS256",
    )

    return jsonify({"token": token, "user": user.to_dict()}), 200
