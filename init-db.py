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
    needs_seed = False
    try:
        from app.models import User, Course, Blog

        # Check if database is empty
        user_count = User.query.count()
        course_count = Course.query.count()
        blog_count = Blog.query.count()

        if user_count == 0 and course_count == 0 and blog_count == 0:
            needs_seed = True
            print("Database is empty, will seed after migrations")
        else:
            print(
                f"✓ Database already has data ({user_count} users, {course_count} courses, {blog_count} blogs)"
            )
    except:
        print("Setting up database...")
        needs_seed = True
        try:
            migrate(message="Initial migration")
        except:
            print("Migration already exists or not needed")

        upgrade()
        print("✓ Database schema created")

    # Seed data if needed
    if needs_seed:
        print("Seeding database...")
        exec(open("app/seed.py").read())
        print("✓ Database seeded")
