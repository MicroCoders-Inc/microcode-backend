from app import create_app
from app.database import db
from app.models import User, Course, Blog
from faker import Faker
from decimal import Decimal
import random

quantity = 50  
fake = Faker()
app = create_app()

with app.app_context():
    print("Seeding database...")

    # Create 50 fake users
    print("Creating 50 users...")
    for _ in range(quantity):
        user = User(username=fake.unique.user_name(), email=fake.unique.email())
        db.session.add(user)


    print("Creating courses with specific topics...")
    topics = [
        "frontend",
        "backend",
        "sql",
        "git"
    ]
    languages = ["English", "Spanish"]
    levels = ["Beginner", "Intermediate", "Advanced"]


    for topic in topics:
        if topic == "frontend":
            course_names = ["React Basics", "CSS Basics", "HTML Basics", "JavaScript Basics"]
        elif topic == "backend":
            course_names = ["Python Basics", "Flask Basics"]
        elif topic == "sql":
            course_names = ["SQL Basics", "SQLAlchemy Basics", "SQLite Basics", "PostgreSQL Basics"]
        elif topic == "git":
            course_names = ["GitHub Basics", "Git CLI Basics", "GitHub Projects Basics"]

        for name in course_names:
            course = Course(
                name=name,
                price=Decimal(str(round(random.uniform(9.99, 99.99), 2))),
                discount=Decimal(str(round(random.uniform(0, 50), 2))),
                language=random.choice(languages),
                topic=topic,
                level=random.choice(levels),
            )
            db.session.add(course)

    # Create 50 fake blogs
    print("Creating 50 blogs...")
    for _ in range(quantity):
        blog = Blog(
            author_name=fake.name(),
            email=fake.email(),
            url=fake.url(),
            description=fake.sentence(nb_words=12),
        )
        db.session.add(blog)

    db.session.commit()
    print("✓ Done! Created 50 users, 50 courses, and 50 blogs.")
