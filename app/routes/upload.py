import os
import uuid
import logging
from flask import Blueprint, jsonify, request
from werkzeug.utils import secure_filename
from app.database import db
from app.models import User
from app.auth_middleware import token_required, verify_user_authorization

from app.constants import MAX_FILE_SIZE, ALLOWED_IMAGE_EXTENSIONS

upload_bp = Blueprint("upload", __name__)
logger = logging.getLogger(__name__)

# Configuration
UPLOAD_FOLDER = "app/static/uploads/profile_pictures"
ALLOWED_EXTENSIONS = ALLOWED_IMAGE_EXTENSIONS

# Ensure upload directory exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@upload_bp.route("/upload/profile-picture/<int:user_id>", methods=["POST"])
@token_required
def upload_profile_picture(current_user_id, user_id):
    # Verify user can only upload their own profile picture
    error = verify_user_authorization(current_user_id, user_id, "upload your own profile picture")
    if error:
        return error

    # Check if user exists
    user = User.query.get_or_404(user_id)

    # Check if file is in request
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]

    # Check if file was selected
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    # Check file size
    file.seek(0, os.SEEK_END)
    file_size = file.tell()
    file.seek(0)

    if file_size > MAX_FILE_SIZE:
        return jsonify({"error": "File size exceeds 5MB limit"}), 400

    # Check if file type is allowed
    if not allowed_file(file.filename):
        return (
            jsonify(
                {
                    "error": f"File type not allowed. Allowed types: {', '.join(ALLOWED_EXTENSIONS)}"
                }
            ),
            400,
        )

    # Secure the filename and extract extension
    secured_filename = secure_filename(file.filename)
    if not secured_filename or "." not in secured_filename:
        return jsonify({"error": "Invalid filename"}), 400

    file_extension = secured_filename.rsplit(".", 1)[1].lower()
    unique_filename = f"{user_id}_{uuid.uuid4().hex}.{file_extension}"
    filepath = os.path.join(UPLOAD_FOLDER, unique_filename)

    # Delete old profile picture if exists
    if user.profile_picture:
        old_filepath = os.path.join("app/static", user.profile_picture.lstrip("/"))
        if os.path.exists(old_filepath):
            try:
                os.remove(old_filepath)
            except Exception as e:
                logger.warning(f"Error deleting old profile picture: {e}")

    # Save file
    try:
        file.save(filepath)
    except Exception as e:
        return jsonify({"error": f"Failed to save file: {str(e)}"}), 500

    # Update user profile picture URL
    profile_picture_url = f"/static/uploads/profile_pictures/{unique_filename}"
    user.profile_picture = profile_picture_url
    db.session.commit()

    return (
        jsonify(
            {
                "message": "Profile picture uploaded successfully",
                "profile_picture": profile_picture_url,
                "user": user.to_dict(),
            }
        ),
        200,
    )


@upload_bp.route("/upload/profile-picture/<int:user_id>", methods=["DELETE"])
@token_required
def delete_profile_picture(current_user_id, user_id):
    # Verify user can only delete their own profile picture
    error = verify_user_authorization(current_user_id, user_id, "delete your own profile picture")
    if error:
        return error

    user = User.query.get_or_404(user_id)

    if not user.profile_picture:
        return jsonify({"error": "No profile picture to delete"}), 404

    # Delete file from filesystem
    filepath = os.path.join("app/static", user.profile_picture.lstrip("/"))
    if os.path.exists(filepath):
        try:
            os.remove(filepath)
        except Exception as e:
            return jsonify({"error": f"Failed to delete file: {str(e)}"}), 500

    # Update user
    user.profile_picture = None
    db.session.commit()

    return (
        jsonify(
            {"message": "Profile picture deleted successfully", "user": user.to_dict()}
        ),
        200,
    )
