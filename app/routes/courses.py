from flask import Blueprint, jsonify

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    return jsonify({"status": "ok"})
        