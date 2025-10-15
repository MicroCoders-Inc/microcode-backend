from flask import jsonify
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
        return jsonify({"error": "Internal server error"}), 500

    @app.errorhandler(IntegrityError)
    def handle_integrity_error(error):
        return jsonify({"error": "Database integrity error"}), 409

    @app.errorhandler(Exception)
    def handle_exception(error):
        return jsonify({"error": "An unexpected error occurred"}), 500
