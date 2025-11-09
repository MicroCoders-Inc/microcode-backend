"""
Script to list all users in the database
"""
from app import create_app
from app.database import db
from app.models import User

app = create_app()

with app.app_context():
    users = User.query.all()

    print(f"\nFound {len(users)} users in database:\n")
    for user in users:
        role = getattr(user, 'role', 'N/A')
        print(f"ID: {user.id}, Username: {user.username}, Email: {user.email}, Role: {role}")
