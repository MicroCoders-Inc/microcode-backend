from app import create_app
from app.database import db
from app.models import User, Course, Blog
from faker import Faker
from decimal import Decimal
import random
import re

fake = Faker()
app = create_app()

TAG_COLOR_REGISTRY = {
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "JavaScript": "#C9AF00",
    "React": "#17829C",
    "JSX": "#6A53C4",
    "Bootstrap": "#7952B3",
    "Tailwind": "#0F8CB8",
    "UI/UX": "#C12675",
    "Accessibility": "#138F6F",
    "Python": "#3776AB",
    "Flask": "#2C3E50",
    "Node.js": "#3C873A",
    "Express.js": "#495057",
    "REST API": "#0D6EFD",
    "Auth": "#DC3545",
    "API Design": "#0A6D8F",
    "Django": "#092E20",
    "Django REST Framework": "#7A0000",
    "SQL": "#0064A5",
    "PostgreSQL": "#27506D",
    "SQLite": "#0F5C96",
    "Migrations": "#C35900",
    "SQLAlchemy": "#6C2F82",
    "ORM": "#4A27AD",
    "Git": "#F05033",
    "GitHub": "#2F81F7",
    "GitHub Projects": "#1E6F36",
    "Branching": "#146C43",
    "Merge Conflicts": "#C13E5D",
    "Git Flow": "#C67800",
}

TOPIC_TAGS = {
    "frontend": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "JSX",
        "Bootstrap",
        "Tailwind",
        "UI/UX",
        "Accessibility",
    ],
    "backend": [
        "Python",
        "Flask",
        "Node.js",
        "Express.js",
        "REST API",
        "Auth",
        "API Design",
        "Django",
        "Django REST Framework",
    ],
    "database": [
        "SQL",
        "PostgreSQL",
        "SQLite",
        "Migrations",
        "SQLAlchemy",
        "ORM",
    ],
    "git": [
        "Git",
        "GitHub",
        "GitHub Projects",
        "Branching",
        "Merge Conflicts",
        "Git Flow",
    ],
}

FRONTEND_COURSES = [
    "HTML Landing Pages",
    "CSS Flexbox Mastery",
    "CSS Grid Layouts",
    "JavaScript DOM Basics",
    "DOM Event Handling",
    "React Components 101",
    "React Hooks Crash",
    "Bootstrap UI Components",
    "Tailwind Utility Guide",
    "Form Validation JS",
    "Frontend Accessibility",
    "React Router Basics",
    "Frontend Debugging",
    "Performance Optimization",
    "Bootstrap Form Design",
]

BACKEND_COURSES = [
    "Python Web Backend",
    "Flask REST API",
    "JWT Auth Flask",
    "Flask Blueprint Basics",
    "Node Fundamentals",
    "Express Routing Patterns",
    "Express Middleware",
    "REST Error Handling",
    "File Upload APIs",
    "Django Model Basics",
    "Django Views Routing",
    "DRF Serializers Intro",
    "API Auth Patterns",
    "API Rate Limiting",
    "Flask Webhooks",
]

DATABASE_COURSES = [
    "SQL Fundamentals",
    "SQL Joins Mastery",
    "SQL Aggregations",
    "PostgreSQL Setup",
    "SQLite Prototyping",
    "SQLAlchemy Models",
    "SQLAlchemy Relations",
    "Alembic Migrations",
    "Transaction Handling",
    "Data Seeding",
    "Data Validation",
    "Database Design",
    "Many To Many",
    "Database Security",
    "Query Optimization",
]

GIT_COURSES = [
    "Git Basics",
    "Branching Strategies",
    "GitHub Pull Requests",
    "Merge Conflicts",
    "Interactive Rebase",
    "Git Tags Releases",
    "Team Git Workflow",
    "GitHub Actions Intro",
    "Monorepo Workflow",
    "Submodule Management",
    "Git Bisect Debugging",
    "Stash Patch Workflow",
    "Git Hooks",
    "Code Review Workflow",
    "GitHub Projects",
]


def build_tags_for_course(topic: str) -> list[dict[str, str]]:
    topic_labels = TOPIC_TAGS.get(topic, [])
    pick_count = min(len(topic_labels), random.randint(2, 4))
    picked = random.sample(topic_labels, k=pick_count)
    return [{"label": label, "color": TAG_COLOR_REGISTRY[label]} for label in picked]


def slugify(name: str) -> str:
    s = name.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = s.strip("-")
    return s


def image_for(name: str, topic: str) -> tuple[str, str]:
    url = "https://placehold.co/400x225"
    alt = f"{topic.capitalize()} course – {name}"
    return url, alt


with app.app_context():
    print("Seeding database...")

    for name in FRONTEND_COURSES:
        course = Course.query.filter_by(name=name).first()
        if not course:
            img_url, img_alt = image_for(name, "frontend")
            db.session.add(
                Course(
                    name=name,
                    price=Decimal(str(round(random.uniform(4.99, 9.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 40), 2))),
                    topic="frontend",
                    level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    tags=build_tags_for_course("frontend"),
                    image_url=img_url,
                    image_alt=img_alt,
                )
            )
        else:
            if course.image_url is None or course.image_alt is None:
                img_url, img_alt = image_for(name, "frontend")
                course.image_url = img_url
                course.image_alt = img_alt

    for name in BACKEND_COURSES:
        course = Course.query.filter_by(name=name).first()
        if not course:
            img_url, img_alt = image_for(name, "backend")
            db.session.add(
                Course(
                    name=name,
                    price=Decimal(str(round(random.uniform(4.99, 9.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 40), 2))),
                    topic="backend",
                    level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    tags=build_tags_for_course("backend"),
                    image_url=img_url,
                    image_alt=img_alt,
                )
            )
        else:
            if course.image_url is None or course.image_alt is None:
                img_url, img_alt = image_for(name, "backend")
                course.image_url = img_url
                course.image_alt = img_alt

    for name in DATABASE_COURSES:
        course = Course.query.filter_by(name=name).first()
        if not course:
            img_url, img_alt = image_for(name, "database")
            db.session.add(
                Course(
                    name=name,
                    price=Decimal(str(round(random.uniform(4.99, 9.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 40), 2))),
                    topic="database",
                    level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    tags=build_tags_for_course("database"),
                    image_url=img_url,
                    image_alt=img_alt,
                )
            )
        else:
            if course.image_url is None or course.image_alt is None:
                img_url, img_alt = image_for(name, "database")
                course.image_url = img_url
                course.image_alt = img_alt

    for name in GIT_COURSES:
        course = Course.query.filter_by(name=name).first()
        if not course:
            img_url, img_alt = image_for(name, "git")
            db.session.add(
                Course(
                    name=name,
                    price=Decimal(str(round(random.uniform(4.99, 9.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 40), 2))),
                    topic="git",
                    level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    tags=build_tags_for_course("git"),
                    image_url=img_url,
                    image_alt=img_alt,
                )
            )
        else:
            if course.image_url is None or course.image_alt is None:
                img_url, img_alt = image_for(name, "git")
                course.image_url = img_url
                course.image_alt = img_alt

  
    for _ in range(50):
        email = fake.unique.email()
        existing_blog = Blog.query.filter_by(email=email).first()
        if not existing_blog:
            db.session.add(
                Blog(
                    author_name=fake.name(),
                    email=email,
                    url=fake.url(),
                    description=fake.sentence(nb_words=12),
                )
            )

    db.session.commit()

    all_course_ids = [course.id for course in Course.query.all()]
    all_blog_ids = [blog.id for blog in Blog.query.all()]

    for _ in range(50):
        username = fake.unique.user_name()
        email = fake.unique.email()
        existing_user = User.query.filter_by(email=email).first()
        if not existing_user:
           
            owned_courses = random.sample(
                all_course_ids, k=random.randint(0, min(8, len(all_course_ids)))
            )
            favourite_courses = random.sample(
                all_course_ids, k=random.randint(0, min(5, len(all_course_ids)))
            )
            saved_blogs = random.sample(
                all_blog_ids, k=random.randint(0, min(10, len(all_blog_ids)))
            )

            db.session.add(
                User(
                    username=username,
                    email=email,
                    owned_courses=owned_courses,
                    favourite_courses=favourite_courses,
                    saved_blogs=saved_blogs,
                )
            )

    db.session.commit()
    print("✓ Done.")