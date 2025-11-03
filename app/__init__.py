import os
from dotenv import load_dotenv
from flask import Flask, send_from_directory
from flask_cors import CORS
from app.database import db, migrate
from app.routes import register_blueprints
from app.errors import register_error_handlers

load_dotenv()


def create_app():
    app = Flask(__name__, static_folder="static")

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5MB max file size

    CORS(app)

    db.init_app(app)
    migrate.init_app(app, db)

    register_blueprints(app)
    register_error_handlers(app)

    # Serve static files
    @app.route("/static/<path:filename>")
    def serve_static(filename):
        return send_from_directory(app.static_folder, filename)

    with app.app_context():
        db.create_all()

    return app
