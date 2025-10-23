from flask import Blueprint, jsonify, make_response
from app.models import Blog
from app.models import Course


index_bp = Blueprint("index", __name__)


@index_bp.route("/", methods=["GET"])
def welcome():
    return jsonify({"msg": "Welcome!"})


@index_bp.route("/favicon.ico", methods=["GET"])
def favicon():
    return make_response("", 204)

@index_bp.route('/home-data', methods=['GET'])
def get_home_data():

    courses = Course.query.limit(4).all()
    blogs = Blog.query.limit(4).all()

    data = {
        "courses": [course.to_dict() for course in courses],
        "blogs": [blog.to_dict() for blog in blogs]
        }
    return jsonify(data)