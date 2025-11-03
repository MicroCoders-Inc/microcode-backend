from app.routes.index import index_bp
from app.routes.health import health_bp
from app.routes.auth import auth_bp
from app.routes.users import users_bp
from app.routes.courses import courses_bp
from app.routes.blogs import blogs_bp
from app.routes.shops import shops_bp
from app.routes.articles import articles_bp
from app.routes.contacts import contacts_bp
from app.routes.upload import upload_bp


def register_blueprints(app):
    app.register_blueprint(index_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(users_bp)
    app.register_blueprint(courses_bp)
    app.register_blueprint(blogs_bp)
    app.register_blueprint(shops_bp)
    app.register_blueprint(articles_bp)
    app.register_blueprint(contacts_bp)
    app.register_blueprint(upload_bp)
