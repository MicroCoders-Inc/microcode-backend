from flask import Blueprint, jsonify

articles_bp = Blueprint("articles", __name__)


@articles_bp.route("/articles", methods=["GET"])
def get_blogs():
    return jsonify({"status": "ok"})
