import traceback
from flask import jsonify, current_app
from sqlalchemy.exc import IntegrityError

def register_error_handlers(app):
    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({"error": "Bad request"}), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({"error": "Method not allowed"}), 405

    @app.errorhandler(409)
    def conflict(error):
        return jsonify({"error": "Conflict"}), 409

    @app.errorhandler(500)
    def internal_error(error):
        response = {"error": "Internal server error"}
        if current_app.config.get("DEBUG", False):
            response["message"] = str(error)
            response["traceback"] = traceback.format_exc()
        return jsonify(response), 500

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        response = {"error": "Database integrity error"}
        if current_app.config.get("DEBUG", False):
            response["message"] = str(error.orig)
            response["statement"] = str(error.statement)
        return jsonify(response), 409

    @app.errorhandler(Exception)
    def handle_exception(error):
        response = {"error": "An unexpected error occurred"}
        if current_app.config.get("DEBUG", False):
            response["type"] = type(error).__name__
            response["message"] = str(error)
            response["traceback"] = traceback.format_exc()
        return jsonify(response), 500