from flask import Blueprint, jsonify
from app.models import Course

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return jsonify(
        {
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/frontend", methods=["GET"])
def get_frontend_courses():
    courses = Course.query.filter_by(topic="frontend").all()
    return jsonify(
        {
            "topic": "frontend",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/backend", methods=["GET"])
def get_backend_courses():
    courses = Course.query.filter_by(topic="backend").all()
    return jsonify(
        {
            "topic": "backend",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/database", methods=["GET"])
def get_database_courses():
    courses = Course.query.filter_by(topic="database").all()
    return jsonify(
        {
            "topic": "database",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )


@courses_bp.route("/courses/git", methods=["GET"])
def get_git_courses():
    courses = Course.query.filter_by(topic="git").all()
    return jsonify(
        {
            "topic": "git",
            "count": len(courses),
            "courses": [course.to_dict() for course in courses],
        }
    )
