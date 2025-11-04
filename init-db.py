"""
One-time database initialization script for Render deployment.
This will run migrations and seed data if tables don't exist.
"""

import os
from app import create_app
from app.database import db
from flask_migrate import Migrate, init, migrate, upgrade

app = create_app()

with app.app_context():
    # Check if migrations directory exists
    migrations_dir = os.path.join(os.path.dirname(__file__), "migrations")

    if not os.path.exists(migrations_dir):
        print("Initializing Flask-Migrate...")
        init()

    # Check if tables exist by trying to query
    try:
        from app.models import User

        User.query.first()
        print("✓ Database already initialized")
    except:
        print("Setting up database...")
        try:
            migrate(message="Initial migration")
        except:
            print("Migration already exists or not needed")

        upgrade()
        print("✓ Database schema created")

        # Seed data
        print("Seeding database...")
        from app import seed

        print("✓ Database seeded")
