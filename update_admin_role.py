"""
Script to update existing admin user to have role='admin'
Run this once after adding the role field to the User model.
"""
from app import create_app
from app.database import db
from app.models import User
import os

app = create_app()

with app.app_context():
    # Get admin email from environment variable
    admin_email = os.getenv("ADMIN_EMAIL", "admin@microcode.com")

    # Find the admin user
    admin_user = User.query.filter_by(email=admin_email).first()

    if admin_user:
        # Update role to admin
        admin_user.role = "admin"
        db.session.commit()
        print(f"✓ Updated user '{admin_user.username}' ({admin_email}) to have role='admin'")
    else:
        print(f"✗ Admin user with email '{admin_email}' not found in database")
        print("\nYou may need to:")
        print("1. Check if ADMIN_EMAIL in .env matches your existing admin user")
        print("2. Or run: pipenv run db-seed to create the admin user")
