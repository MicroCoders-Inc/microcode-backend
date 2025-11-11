"""
Migration script to add color properties to course tags.

This script updates existing course tags in the database to include
color properties based on the TAG_COLOR_REGISTRY.
"""

from app import create_app
from app.database import db
from app.models import Course

# TAG_COLOR_REGISTRY - same as in seed.py
TAG_COLOR_REGISTRY = {
    # Languages & Frameworks
    "HTML": "#E34F26",
    "CSS": "#1572B6",
    "JavaScript": "#D4A017",
    "React": "#0088CC",
    "JSX": "#0088CC",
    "Bootstrap": "#7952B3",
    "Tailwind": "#0891B2",
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
    "Routes": "#0C7FB5",

    # Frontend Concepts
    "Mobile": "#28A745",
    "Styling": "#8E44AD",
    "Events": "#E67E22",
    "DOM": "#C0392B",
    "Semantic": "#16A085",

    # Database Concepts
    "Design": "#229954",
    "Queries": "#0E8E77",
    "Relations": "#9B59B6",
    "Schema": "#34495E",
    "CRUD": "#E67E22",
    "Trans": "#D35400",

    # Git Workflow
    "VCS": "#E67E22",
    "Workflow": "#2980B9",
    "Branch": "#9B59B6",
    "Merge": "#0E8E77",
    "Teams": "#1E8449",
    "Remote": "#0C7FB5",
}

app = create_app()


def normalize_tag_name(tag_name: str) -> str:
    """Normalize tag name for matching against registry."""
    return tag_name.strip().title()


def get_color_for_tag(tag_name: str) -> str:
    """Get color for a tag name from the registry."""
    # Try exact match first
    if tag_name in TAG_COLOR_REGISTRY:
        return TAG_COLOR_REGISTRY[tag_name]

    # Try case-insensitive match
    for registry_name, color in TAG_COLOR_REGISTRY.items():
        if registry_name.lower() == tag_name.lower():
            return color

    # Default color if not found
    return "#6C757D"


def migrate_tags():
    """Update all course tags to include color properties."""
    with app.app_context():
        print("Starting tag migration...")

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
                # Extract tag name/label
                if isinstance(tag, dict):
                    tag_name = tag.get("label") or tag.get("name") or str(tag)
                    current_color = tag.get("color")
                else:
                    tag_name = str(tag)
                    current_color = None

                # Normalize the tag name for the registry
                normalized_name = normalize_tag_name(tag_name)
                correct_color = get_color_for_tag(normalized_name)

                # Check if tag needs update (no color, or color doesn't match registry)
                if current_color != correct_color:
                    needs_update = True
                    # Create updated tag with both label and color
                    updated_tag = {
                        "label": normalized_name,
                        "color": correct_color
                    }
                    updated_tags.append(updated_tag)

                    if current_color:
                        print(f"  - {course.name}: Updated tag '{tag_name}' color from {current_color} -> {correct_color}")
                    else:
                        print(f"  - {course.name}: Added color to tag '{tag_name}' (color: {correct_color})")
                else:
                    # Tag already has correct color
                    updated_tags.append(tag)

            if needs_update:
                # Update the course tags
                course.tags = updated_tags
                updated_count += 1
                print(f"  ✓ Updated {course.name}")
            else:
                unchanged_count += 1
                print(f"  - {course.name}: Already has colors, skipping")

        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\n✓ Migration complete!")
            print(f"  - Updated: {updated_count} courses")
            print(f"  - Unchanged: {unchanged_count} courses")
        else:
            print(f"\n✓ No courses needed updating")
            print(f"  - All {unchanged_count} courses already have colored tags")


if __name__ == "__main__":
    migrate_tags()
