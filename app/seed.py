from app import create_app
from app.database import db
from app.models import User
from faker import Faker

fake = Faker()
app = create_app()

with app.app_context():
    print("Creating 10 fake users...")

    for _ in range(10):
        user = User(username=fake.unique.user_name(), email=fake.unique.email())
        db.session.add(user)

    db.session.commit()
    print("✓ Done!")
