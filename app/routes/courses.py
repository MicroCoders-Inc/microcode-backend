from flask import Blueprint, jsonify
from app.models import Course

courses_bp = Blueprint("courses", __name__)


@courses_bp.route("/courses", methods=["GET"])
def get_courses():
    return jsonify({"status": "ok"})



@courses_bp.route("/courses/frontend", methods=["GET"])
def get_frontend_courses():
    frontend_courses = Course.query.filter_by(topic="frontend").all()
    return jsonify({"topic": "frontend", "courses": [course.to_dict() for course in frontend_courses]})

@courses_bp.route("/courses/backend", methods=["GET"])
def get_backend_courses():
    backend_courses = Course.query.filter_by(topic="backend").all()
    return jsonify({"topic": "backend", "courses": [course.to_dict() for course in backend_courses]})

@courses_bp.route("/courses/sql", methods=["GET"])
def get_sql_courses():
    sql_courses = Course.query.filter_by(topic="sql").all()
    return jsonify({"topic": "sql", "courses": [course.to_dict() for course in sql_courses]})

@courses_bp.route("/courses/git", methods=["GET"])
def get_git_courses():
    git_courses = Course.query.filter_by(topic="git").all()
    return jsonify({"topic": "git", "courses": [course.to_dict() for course in git_courses]})