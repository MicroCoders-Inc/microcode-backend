from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Contact
from app.validation import validate_email, validate_string_field
from app.constants import MAX_CONTACT_MESSAGE_LENGTH

contacts_bp = Blueprint("contacts", __name__)

@contacts_bp.route("/contacts", methods=["POST"])
def post_messages():
    data = request.get_json()

    # Validate email
    is_valid, error = validate_email(data.get("email"))
    if not is_valid:
        return jsonify({"error": error}), 400

    # Validate message
    is_valid, error = validate_string_field(data.get("messages"), "Message", MAX_CONTACT_MESSAGE_LENGTH)
    if not is_valid:
        return jsonify({"error": error}), 400

    new_messages = Contact(
        email=data.get("email"),
        messages=data.get("messages")
    )
    db.session.add(new_messages)
    db.session.commit()
    return jsonify(new_messages.to_dict()), 201