from flask import Blueprint, jsonify

blogs_bp = Blueprint("blogs", __name__)


@blogs_bp.route("/blogs", methods=["GET"])
def get_blogs():
    return jsonify({"status": "ok"})
