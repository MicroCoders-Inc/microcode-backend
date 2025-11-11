"""
Script to check current tags for all courses.
"""

from app import create_app
from app.models import Course

app = create_app()

with app.app_context():
    courses = Course.query.all()

    print("Current tags per course:\n")
    print("=" * 80)

    for course in courses:
        tag_labels = [tag.get("label", "?") for tag in course.tags] if course.tags else []
        tag_count = len(tag_labels)

        print(f"\n{course.name}")
        print(f"  Topic: {course.topic}")
        print(f"  Tag count: {tag_count}")
        print(f"  Tags: {', '.join(tag_labels)}")

        if tag_count > 3:
            print(f"  ⚠️  EXCEEDS 3 TAGS")
