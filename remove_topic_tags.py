"""
Migration script to remove topic tags (Frontend, Backend, Database) from course tags.
These are redundant since courses already have a 'topic' field.
"""

from app import create_app
from app.database import db
from app.models import Course

app = create_app()

# Topic tags to remove (redundant with course.topic field)
TOPIC_TAGS = ["Frontend", "Backend", "Database"]


def remove_topic_tags():
    """Remove topic tags from all courses."""
    with app.app_context():
        print("Starting topic tag removal...")

        # Get all courses
        courses = Course.query.all()
        print(f"Found {len(courses)} courses to process")

        updated_count = 0
        unchanged_count = 0

        for course in courses:
            if not course.tags:
                print(f"  - {course.name}: No tags, skipping")
                unchanged_count += 1
                continue

            original_tag_count = len(course.tags)

            # Filter out topic tags (case-insensitive)
            filtered_tags = [
                tag for tag in course.tags
                if isinstance(tag, dict) and tag.get("label") not in TOPIC_TAGS
            ]

            if len(filtered_tags) < original_tag_count:
                removed_count = original_tag_count - len(filtered_tags)
                course.tags = filtered_tags
                updated_count += 1
                print(f"  ✓ {course.name}: Removed {removed_count} topic tag(s), {len(filtered_tags)} tags remaining")
            else:
                unchanged_count += 1
                print(f"  - {course.name}: No topic tags found, skipping")

        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\n✓ Migration complete!")
            print(f"  - Updated: {updated_count} courses")
            print(f"  - Unchanged: {unchanged_count} courses")
        else:
            print(f"\n✓ No courses needed updating")
            print(f"  - All {unchanged_count} courses already have no topic tags")


if __name__ == "__main__":
    remove_topic_tags()
