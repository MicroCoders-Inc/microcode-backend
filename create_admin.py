"""
Script to create admin user from environment variables
Safe to run multiple times - checks if admin exists first
"""
from app import create_app
from app.database import db
from app.models import User
from werkzeug.security import generate_password_hash
import os

app = create_app()

with app.app_context():
    # Get admin credentials from environment variables
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    # Check if admin already exists
    admin_user = User.query.filter_by(email=admin_email).first()

    if admin_user:
        print(f"✓ Admin user already exists: {admin_user.username} ({admin_email})")
        # Update role to admin if it's not already
        if admin_user.role != "admin":
            admin_user.role = "admin"
            db.session.commit()
            print(f"✓ Updated role to 'admin'")
    else:
        # Create new admin user
        print(f"Creating admin user: {admin_username} ({admin_email})...")
        new_admin = User(
            username=admin_username,
            email=admin_email,
            password_hash=generate_password_hash(admin_password),
            role="admin",
            owned_courses=[],
            favourite_courses=[],
            saved_blogs=[],
        )
        db.session.add(new_admin)
        db.session.commit()
        print(f"✓ Admin user created successfully!")
        print(f"\nLogin credentials:")
        print(f"  Email: {admin_email}")
        print(f"  Password: {admin_password}")
