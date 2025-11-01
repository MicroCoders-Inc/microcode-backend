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

    # --- USERS ---
    print("Creating 50 users (if not already exist)...")
    for _ in range(quantity):
        username = fake.unique.user_name()
        email = fake.unique.email()
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
            db.session.add(User(username=username, email=email))

    # --- COURSES ---
    print("Creating courses with specific topics (avoiding duplicates)...")

    topics = ["frontend", "backend", "sql", "git"]
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
        else:
            course_names = []

        for name in course_names:
            existing_course = Course.query.filter_by(name=name).first()
            if not existing_course:
                course = Course(
                    name=name,
                    price=Decimal(str(round(random.uniform(9.99, 99.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 50), 2))),
                    language=random.choice(languages),
                    topic=topic,
                    level=random.choice(levels),
                )
                db.session.add(course)

    # --- BLOGS ---
    print("Creating 50 blogs (if not already exist)...")
    for _ in range(quantity):
        email = fake.unique.email()
        existing_blog = Blog.query.filter_by(email=email).first()
        if not existing_blog:
            blog = Blog(
                author_name=fake.name(),
                email=email,
                url=fake.url(),
                description=fake.sentence(nb_words=12),
            )
            db.session.add(blog)

    # --- COMMIT ---
    db.session.commit()
    print("✓ Done! Database seeding complete without duplicates.")
