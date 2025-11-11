"""
Migration script to limit each course to exactly 5 most relevant tags.
Home page will still only display 3 tags via slice(0, 3).
"""

from app import create_app
from app.database import db
from app.models import Course

app = create_app()

# TAG_COLOR_REGISTRY for reference
TAG_COLOR_REGISTRY = {
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
    "SQL": "#0064A5",
    "PostgreSQL": "#4169E1",
    "SQLite": "#003B57",
    "SQLAlchemy": "#D71F00",
    "ORM": "#6C757D",
    "Git": "#F05032",
    "GitHub": "#181717",
    "CLI": "#4EAA25",
    "REST API": "#0D6EFD",
    "Auth": "#DC3545",
    "JWT": "#E74C3C",
    "Routes": "#0C7FB5",
    "Mobile": "#28A745",
    "Styling": "#8E44AD",
    "Events": "#E67E22",
    "DOM": "#C0392B",
    "Semantic": "#16A085",
    "Design": "#229954",
    "Queries": "#0E8E77",
    "Relations": "#9B59B6",
    "Schema": "#34495E",
    "CRUD": "#E67E22",
    "Trans": "#D35400",
    "VCS": "#E67E22",
    "Workflow": "#2980B9",
    "Branch": "#9B59B6",
    "Merge": "#0E8E77",
    "Teams": "#1E8449",
    "Remote": "#0C7FB5",
}

# Manual curation: specify exactly which 5 tags each course should have
# Most important tags first (first 3 will show on home page)
COURSE_TAG_SELECTIONS = {
    "HTML Fundamentals": ["HTML", "Semantic", "DOM", "Styling", "Mobile"],
    "CSS Styling and Layout": ["CSS", "Styling", "Mobile", "HTML", "DOM"],
    "JavaScript Fundamentals": ["JavaScript", "Events", "DOM", "HTML", "CSS"],
    "Python for Backend": ["Python", "CLI", "Routes", "Auth", "Flask"],
    "Flask Models with SQLAlchemy": ["Flask", "SQLAlchemy", "ORM", "Python", "SQL"],
    "Flask Blueprints and Routes": ["Flask", "Routes", "JWT", "Auth", "Python"],
    "SQL Fundamentals": ["SQL", "Queries", "CRUD", "Schema", "Design"],
    "SQL Table Design and Relationships": ["SQL", "Design", "Relations", "Schema", "Queries"],
    "SQL Data Manipulation and Transactions": ["SQL", "CRUD", "Trans", "Queries", "Schema"],
    "Git Basics": ["Git", "VCS", "CLI", "Workflow", "Branch"],
    "Git Branching and Merging": ["Git", "Branch", "Merge", "VCS", "Workflow"],
    "Git with GitHub and Collaboration": ["Git", "GitHub", "Teams", "Remote", "Branch"],
}


def limit_tags_to_5():
    """Limit each course to exactly 5 most relevant tags."""
    with app.app_context():
        print("Starting 5-tag limit migration...")

        courses = Course.query.all()
        print(f"Found {len(courses)} courses to process\n")

        updated_count = 0

        for course in courses:
            # Get the curated tag selection for this course
            selected_tag_labels = COURSE_TAG_SELECTIONS.get(course.name)

            if not selected_tag_labels:
                print(f"  ⚠️  {course.name}: No tag selection defined, skipping")
                continue

            # Build new tag list with proper capitalization and colors
            new_tags = []
            for label in selected_tag_labels:
                color = TAG_COLOR_REGISTRY.get(label, "#6C757D")
                new_tags.append({
                    "label": label,
                    "color": color
                })

            # Update course tags
            old_tag_labels = [tag.get("label", "?") for tag in (course.tags or [])]
            course.tags = new_tags
            updated_count += 1

            print(f"  ✓ {course.name}")
            print(f"    Old tags ({len(old_tag_labels)}): {', '.join(old_tag_labels)}")
            print(f"    New tags (5): {', '.join(selected_tag_labels)}")
            print(f"    Home page display: {', '.join(selected_tag_labels[:3])}")

        # Commit all changes
        if updated_count > 0:
            db.session.commit()
            print(f"\n✓ Migration complete!")
            print(f"  - Updated: {updated_count} courses")
            print(f"  - All courses now have exactly 5 relevant tags")
            print(f"  - Home page will display first 3 tags via slice(0, 3)")
        else:
            print(f"\n⚠️  No courses were updated")


if __name__ == "__main__":
    limit_tags_to_5()
