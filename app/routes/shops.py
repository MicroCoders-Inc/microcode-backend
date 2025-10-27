from flask import Blueprint, jsonify

shops_bp = Blueprint("shops", __name__)


@shops_bp.route("/shops", methods=["GET"])
def get_shops():
    return jsonify({"status": "ok"})
        