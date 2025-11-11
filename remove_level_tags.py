"""
Migration script to remove level tags (Beginner, Intermediate, Advanced) from course tags.
"""

from app import create_app
from app.database import db
from app.models import Course

app = create_app()

# Level tags to remove
LEVEL_TAGS = ["Beginner", "Intermediate", "Advanced"]


def remove_level_tags():
    """Remove level tags from all courses."""
    with app.app_context():
        print("Starting level tag removal...")

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

            # Filter out level tags (case-insensitive)
            filtered_tags = [
                tag for tag in course.tags
                if isinstance(tag, dict) and tag.get("label") not in LEVEL_TAGS
            ]

            if len(filtered_tags) < original_tag_count:
                removed_count = original_tag_count - len(filtered_tags)
                course.tags = filtered_tags
                updated_count += 1
                print(f"  ✓ {course.name}: Removed {removed_count} level tag(s), {len(filtered_tags)} tags remaining")
            else:
                unchanged_count += 1
                print(f"  - {course.name}: No level tags found, skipping")

        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\n✓ Migration complete!")
            print(f"  - Updated: {updated_count} courses")
            print(f"  - Unchanged: {unchanged_count} courses")
        else:
            print(f"\n✓ No courses needed updating")
            print(f"  - All {unchanged_count} courses already have no level tags")


if __name__ == "__main__":
    remove_level_tags()
