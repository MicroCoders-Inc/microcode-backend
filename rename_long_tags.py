"""
Migration script to rename long and hyphenated tags to shorter versions.
This makes tags more compact and readable on course cards.
"""

from app import create_app
from app.database import db
from app.models import Course

app = create_app()

# TAG_COLOR_REGISTRY with new names
TAG_COLOR_REGISTRY = {
    # Languages & Frameworks
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "JavaScript": "#F7DF1E",
    "React": "#61DAFB",
    "JSX": "#61DAFB",
    "Bootstrap": "#7952B3",
    "Tailwind": "#06B6D4",
    "Python": "#3776AB",
    "Flask": "#000000",
    "Node.js": "#339933",
    "Express.js": "#000000",
    "Django": "#092E20",

    # Databases & ORM
    "SQL": "#0064A5",
    "PostgreSQL": "#4169E1",
    "SQLite": "#003B57",
    "SQLAlchemy": "#D71F00",
    "ORM": "#6C757D",

    # Git & Version Control
    "Git": "#F05032",
    "GitHub": "#181717",
    "CLI": "#4EAA25",

    # Backend & API
    "REST API": "#0D6EFD",
    "Auth": "#DC3545",
    "JWT": "#E74C3C",
    "Routes": "#5DADE2",

    # Frontend Concepts
    "Mobile": "#28A745",
    "Styling": "#8E44AD",
    "Events": "#E67E22",
    "DOM": "#C0392B",
    "Semantic": "#16A085",

    # Database Concepts
    "Design": "#229954",
    "Queries": "#1ABC9C",
    "Relations": "#9B59B6",
    "Schema": "#34495E",
    "CRUD": "#E67E22",
    "Trans": "#D35400",

    # Git Workflow
    "VCS": "#E67E22",
    "Workflow": "#3498DB",
    "Branch": "#9B59B6",
    "Merge": "#1ABC9C",
    "Teams": "#27AE60",
    "Remote": "#5DADE2",
}

# Mapping of old tag names to new tag names
TAG_RENAME_MAP = {
    "Semantic-Web": "Semantic",
    "API-Rest": None,  # Remove entirely (REST API already exists)
    "Database-Design": "Design",
    "Version-Control": "VCS",
    "Interactivity": "Events",
    "Responsive": "Mobile",
    "Blueprints": "Routes",
    "Relationships": "Relations",
    "Transactions": "Trans",
    "Collaboration": "Teams",
    "Branching": "Branch",
    "Merging": "Merge",
}


def rename_long_tags():
    """Rename long and hyphenated tags to shorter versions."""
    with app.app_context():
        print("Starting tag renaming migration...")

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

            needs_update = False
            updated_tags = []

            for tag in course.tags:
                if not isinstance(tag, dict):
                    updated_tags.append(tag)
                    continue

                tag_label = tag.get("label")

                # Check if this tag needs to be renamed
                if tag_label in TAG_RENAME_MAP:
                    new_label = TAG_RENAME_MAP[tag_label]

                    # If None, remove the tag entirely
                    if new_label is None:
                        needs_update = True
                        print(f"  - {course.name}: Removing tag '{tag_label}'")
                        continue

                    # Rename the tag
                    needs_update = True
                    new_color = TAG_COLOR_REGISTRY.get(new_label, tag.get("color"))
                    updated_tag = {
                        "label": new_label,
                        "color": new_color
                    }
                    updated_tags.append(updated_tag)
                    print(f"  - {course.name}: Renamed '{tag_label}' -> '{new_label}'")
                else:
                    # Keep tag as is
                    updated_tags.append(tag)

            if needs_update:
                # Update the course tags
                course.tags = updated_tags
                updated_count += 1
                print(f"  ✓ Updated {course.name}")
            else:
                unchanged_count += 1

        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\n✓ Migration complete!")
            print(f"  - Updated: {updated_count} courses")
            print(f"  - Unchanged: {unchanged_count} courses")
        else:
            print(f"\n✓ No courses needed updating")
            print(f"  - All {unchanged_count} courses already have short tags")


if __name__ == "__main__":
    rename_long_tags()
