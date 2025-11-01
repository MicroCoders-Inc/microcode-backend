from flask import Blueprint, jsonify, request
from app.database import db
from app.models import Contact

contacts_bp = Blueprint("contacts", __name__)

@contacts_bp.route("/contacts", methods=["POST"])
def post_messages():
    data = request.get_json()
    new_messages = Contact(
        email=data.get("email"),
        messages=data.get("messages")
    )
    db.session.add(new_messages)
    db.session.commit()
    return jsonify(new_messages.to_dict()), 201