from app import create_app
from app.database import db
from app.models import User, Course, Blog
from faker import Faker
from decimal import Decimal
from werkzeug.security import generate_password_hash
import random
import os

fake = Faker()
app = create_app()

TAG_COLOR_REGISTRY = {
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
    "REST API": "#0D6EFD",
    "Auth": "#DC3545",
    "Django": "#092E20",
    "SQL": "#0064A5",
    "PostgreSQL": "#4169E1",
    "SQLite": "#003B57",
    "SQLAlchemy": "#D71F00",
    "ORM": "#6C757D",
    "Git": "#F05032",
    "GitHub": "#181717",
    "CLI": "#4EAA25",
}

# Course definitions - 10 per topic with complete data
FRONTEND_COURSES = [
    {
        "name": "HTML Landing Pages",
        "description": "Learn to build beautiful landing pages with semantic HTML",
        "tags": [
            {"label": "HTML", "color": TAG_COLOR_REGISTRY["HTML"]},
            {"label": "CSS", "color": TAG_COLOR_REGISTRY["CSS"]},
        ],
        "summary": {
            "goal": "Create professional landing pages using modern HTML5 elements",
            "syllabus": [
                "HTML5 semantic elements",
                "Page structure and layout",
                "Forms and input elements",
                "SEO best practices",
                "Accessibility fundamentals",
            ],
            "requirements": [],
        },
    },
    {
        "name": "CSS Flexbox Mastery",
        "description": "Master CSS Flexbox for responsive layouts",
        "tags": [
            {"label": "CSS", "color": TAG_COLOR_REGISTRY["CSS"]},
            {"label": "HTML", "color": TAG_COLOR_REGISTRY["HTML"]},
        ],
        "summary": {
            "goal": "Build flexible, responsive layouts with CSS Flexbox",
            "syllabus": [
                "Flexbox fundamentals",
                "Flex container properties",
                "Flex item properties",
                "Common layout patterns",
                "Responsive design with Flexbox",
            ],
            "requirements": ["HTML Landing Pages"],
        },
    },
    {
        "name": "CSS Grid Layouts",
        "description": "Create complex layouts with CSS Grid",
        "tags": [
            {"label": "CSS", "color": TAG_COLOR_REGISTRY["CSS"]},
            {"label": "HTML", "color": TAG_COLOR_REGISTRY["HTML"]},
        ],
        "summary": {
            "goal": "Master CSS Grid for creating complex, responsive layouts",
            "syllabus": [
                "Grid container and items",
                "Grid template areas",
                "Implicit vs explicit grids",
                "Grid gaps and alignment",
                "Responsive grid patterns",
            ],
            "requirements": ["CSS Flexbox Mastery"],
        },
    },
    {
        "name": "JavaScript DOM Basics",
        "description": "Learn to manipulate the DOM with JavaScript",
        "tags": [
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
            {"label": "HTML", "color": TAG_COLOR_REGISTRY["HTML"]},
        ],
        "summary": {
            "goal": "Master DOM manipulation and create interactive web pages",
            "syllabus": [
                "Selecting DOM elements",
                "Modifying element content and attributes",
                "Creating and removing elements",
                "Event listeners",
                "DOM traversal",
            ],
            "requirements": ["HTML Landing Pages"],
        },
    },
    {
        "name": "DOM Event Handling",
        "description": "Handle user interactions with JavaScript events",
        "tags": [
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
            {"label": "HTML", "color": TAG_COLOR_REGISTRY["HTML"]},
        ],
        "summary": {
            "goal": "Master event handling for interactive web applications",
            "syllabus": [
                "Event types and listeners",
                "Event bubbling and capturing",
                "Event delegation",
                "Preventing default behavior",
                "Custom events",
            ],
            "requirements": ["JavaScript DOM Basics"],
        },
    },
    {
        "name": "React Components 101",
        "description": "Introduction to React components and props",
        "tags": [
            {"label": "React", "color": TAG_COLOR_REGISTRY["React"]},
            {"label": "JSX", "color": TAG_COLOR_REGISTRY["JSX"]},
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
        ],
        "summary": {
            "goal": "Build reusable React components and understand the component lifecycle",
            "syllabus": [
                "What is React & why use it?",
                "JSX syntax",
                "Functional vs class components",
                "Props and state",
                "Component composition",
            ],
            "requirements": ["JavaScript DOM Basics", "DOM Event Handling"],
        },
    },
    {
        "name": "React Hooks Crash",
        "description": "Modern React with Hooks - useState, useEffect, and more",
        "tags": [
            {"label": "React", "color": TAG_COLOR_REGISTRY["React"]},
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
        ],
        "summary": {
            "goal": "Master React Hooks for modern functional components",
            "syllabus": [
                "Introduction to Hooks",
                "useState for state management",
                "useEffect for side effects",
                "useContext for global state",
                "Custom Hooks",
            ],
            "requirements": ["React Components 101"],
        },
    },
    {
        "name": "Bootstrap UI Components",
        "description": "Build responsive UIs quickly with Bootstrap",
        "tags": [
            {"label": "Bootstrap", "color": TAG_COLOR_REGISTRY["Bootstrap"]},
            {"label": "CSS", "color": TAG_COLOR_REGISTRY["CSS"]},
        ],
        "summary": {
            "goal": "Create professional UIs using Bootstrap components",
            "syllabus": [
                "Bootstrap grid system",
                "Navigation components",
                "Cards and modals",
                "Forms and buttons",
                "Utilities and customization",
            ],
            "requirements": ["CSS Flexbox Mastery"],
        },
    },
    {
        "name": "Tailwind Utility Guide",
        "description": "Utility-first CSS with Tailwind",
        "tags": [
            {"label": "Tailwind", "color": TAG_COLOR_REGISTRY["Tailwind"]},
            {"label": "CSS", "color": TAG_COLOR_REGISTRY["CSS"]},
        ],
        "summary": {
            "goal": "Build modern UIs with Tailwind's utility-first approach",
            "syllabus": [
                "Tailwind philosophy",
                "Responsive design utilities",
                "Spacing and sizing",
                "Colors and theming",
                "Custom configurations",
            ],
            "requirements": ["CSS Flexbox Mastery"],
        },
    },
    {
        "name": "React Router Basics",
        "description": "Navigation in React applications",
        "tags": [
            {"label": "React", "color": TAG_COLOR_REGISTRY["React"]},
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
        ],
        "summary": {
            "goal": "Implement client-side routing in React applications",
            "syllabus": [
                "Router setup and configuration",
                "Route definitions and paths",
                "Navigation with Link components",
                "URL parameters and query strings",
                "Nested routes",
            ],
            "requirements": ["React Components 101"],
        },
    },
]

BACKEND_COURSES = [
    {
        "name": "Python Web Backend",
        "description": "Build backend applications with Python",
        "tags": [
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
            {"label": "Flask", "color": TAG_COLOR_REGISTRY["Flask"]},
        ],
        "summary": {
            "goal": "Create robust backend services using Python",
            "syllabus": [
                "Python fundamentals review",
                "Web frameworks overview",
                "HTTP request/response cycle",
                "Routing and views",
                "Working with databases",
            ],
            "requirements": [],
        },
    },
    {
        "name": "Flask REST API",
        "description": "Build RESTful APIs with Flask",
        "tags": [
            {"label": "Flask", "color": TAG_COLOR_REGISTRY["Flask"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
            {"label": "REST API", "color": TAG_COLOR_REGISTRY["REST API"]},
        ],
        "summary": {
            "goal": "Design and implement RESTful APIs using Flask",
            "syllabus": [
                "REST principles",
                "Flask routing for APIs",
                "Request and response handling",
                "JSON serialization",
                "Error handling",
            ],
            "requirements": ["Python Web Backend"],
        },
    },
    {
        "name": "JWT Auth Flask",
        "description": "Implement JWT authentication in Flask",
        "tags": [
            {"label": "Flask", "color": TAG_COLOR_REGISTRY["Flask"]},
            {"label": "Auth", "color": TAG_COLOR_REGISTRY["Auth"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
        ],
        "summary": {
            "goal": "Secure Flask APIs with JWT authentication",
            "syllabus": [
                "Authentication vs authorization",
                "JWT token structure",
                "User registration and login",
                "Protected routes",
                "Token refresh strategies",
            ],
            "requirements": ["Flask REST API"],
        },
    },
    {
        "name": "Flask Blueprint Basics",
        "description": "Organize Flask apps with Blueprints",
        "tags": [
            {"label": "Flask", "color": TAG_COLOR_REGISTRY["Flask"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
        ],
        "summary": {
            "goal": "Structure large Flask applications using Blueprints",
            "syllabus": [
                "What are Blueprints?",
                "Creating and registering Blueprints",
                "Blueprint templates and static files",
                "URL prefixes",
                "Blueprint best practices",
            ],
            "requirements": ["Python Web Backend"],
        },
    },
    {
        "name": "Node Fundamentals",
        "description": "Backend development with Node.js",
        "tags": [
            {"label": "Node.js", "color": TAG_COLOR_REGISTRY["Node.js"]},
            {"label": "JavaScript", "color": TAG_COLOR_REGISTRY["JavaScript"]},
        ],
        "summary": {
            "goal": "Build backend services with Node.js",
            "syllabus": [
                "Node.js runtime basics",
                "Modules and npm",
                "Asynchronous programming",
                "File system operations",
                "Creating HTTP servers",
            ],
            "requirements": [],
        },
    },
    {
        "name": "Express Routing Patterns",
        "description": "Advanced routing in Express.js",
        "tags": [
            {"label": "Express.js", "color": TAG_COLOR_REGISTRY["Express.js"]},
            {"label": "Node.js", "color": TAG_COLOR_REGISTRY["Node.js"]},
        ],
        "summary": {
            "goal": "Master advanced routing patterns in Express",
            "syllabus": [
                "Route parameters and queries",
                "Route handlers and methods",
                "Router middleware",
                "Modular routing",
                "Route validation",
            ],
            "requirements": ["Node Fundamentals"],
        },
    },
    {
        "name": "Express Middleware",
        "description": "Create and use Express middleware",
        "tags": [
            {"label": "Express.js", "color": TAG_COLOR_REGISTRY["Express.js"]},
            {"label": "Node.js", "color": TAG_COLOR_REGISTRY["Node.js"]},
        ],
        "summary": {
            "goal": "Understand and create Express middleware functions",
            "syllabus": [
                "Middleware concept",
                "Built-in middleware",
                "Third-party middleware",
                "Custom middleware",
                "Error handling middleware",
            ],
            "requirements": ["Express Routing Patterns"],
        },
    },
    {
        "name": "Django Model Basics",
        "description": "Django ORM and models",
        "tags": [
            {"label": "Django", "color": TAG_COLOR_REGISTRY["Django"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
        ],
        "summary": {
            "goal": "Define and work with Django models",
            "syllabus": [
                "Django ORM overview",
                "Model fields and types",
                "Model methods",
                "QuerySets and managers",
                "Model relationships",
            ],
            "requirements": [],
        },
    },
    {
        "name": "Django Views Routing",
        "description": "Views and URL routing in Django",
        "tags": [
            {"label": "Django", "color": TAG_COLOR_REGISTRY["Django"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
        ],
        "summary": {
            "goal": "Create views and configure URL routing in Django",
            "syllabus": [
                "Function-based views",
                "Class-based views",
                "URL patterns",
                "URL namespacing",
                "View decorators",
            ],
            "requirements": ["Django Model Basics"],
        },
    },
    {
        "name": "API Auth Patterns",
        "description": "Authentication patterns for APIs",
        "tags": [
            {"label": "Auth", "color": TAG_COLOR_REGISTRY["Auth"]},
            {"label": "REST API", "color": TAG_COLOR_REGISTRY["REST API"]},
        ],
        "summary": {
            "goal": "Implement various authentication patterns for APIs",
            "syllabus": [
                "Basic authentication",
                "Token-based authentication",
                "OAuth 2.0 overview",
                "API keys",
                "Session vs token auth",
            ],
            "requirements": [],
        },
    },
]

DATABASE_COURSES = [
    {
        "name": "SQL Fundamentals",
        "description": "Master SQL basics for database queries",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Write efficient SQL queries for data retrieval and manipulation",
            "syllabus": [
                "Database concepts",
                "SELECT statements",
                "WHERE clauses and filtering",
                "INSERT, UPDATE, DELETE",
                "Basic joins",
            ],
            "requirements": [],
        },
    },
    {
        "name": "SQL Joins Mastery",
        "description": "Master all types of SQL joins",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Master different types of SQL joins",
            "syllabus": [
                "INNER JOIN",
                "LEFT JOIN",
                "RIGHT JOIN",
                "FULL OUTER JOIN",
                "Self joins and cross joins",
            ],
            "requirements": ["SQL Fundamentals"],
        },
    },
    {
        "name": "SQL Aggregations",
        "description": "Aggregate functions and GROUP BY",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Use aggregate functions to analyze data",
            "syllabus": [
                "COUNT, SUM, AVG functions",
                "GROUP BY clause",
                "HAVING clause",
                "Aggregate with joins",
                "Window functions intro",
            ],
            "requirements": ["SQL Fundamentals"],
        },
    },
    {
        "name": "PostgreSQL Setup",
        "description": "Set up and configure PostgreSQL",
        "tags": [
            {"label": "PostgreSQL", "color": TAG_COLOR_REGISTRY["PostgreSQL"]},
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Install and configure PostgreSQL database",
            "syllabus": [
                "PostgreSQL installation",
                "Database creation",
                "User management",
                "psql command line",
                "pgAdmin interface",
            ],
            "requirements": [],
        },
    },
    {
        "name": "SQLite Prototyping",
        "description": "Rapid prototyping with SQLite",
        "tags": [
            {"label": "SQLite", "color": TAG_COLOR_REGISTRY["SQLite"]},
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Use SQLite for rapid application prototyping",
            "syllabus": [
                "SQLite basics",
                "Creating databases",
                "SQLite command line",
                "When to use SQLite",
                "SQLite limitations",
            ],
            "requirements": [],
        },
    },
    {
        "name": "SQLAlchemy Models",
        "description": "Define database models with SQLAlchemy",
        "tags": [
            {"label": "SQLAlchemy", "color": TAG_COLOR_REGISTRY["SQLAlchemy"]},
            {"label": "Python", "color": TAG_COLOR_REGISTRY["Python"]},
        ],
        "summary": {
            "goal": "Define database models using SQLAlchemy ORM",
            "syllabus": [
                "ORM concepts",
                "Defining models",
                "Column types",
                "Table configuration",
                "Sessions and queries",
            ],
            "requirements": ["SQL Fundamentals"],
        },
    },
    {
        "name": "SQLAlchemy Relations",
        "description": "Model relationships in SQLAlchemy",
        "tags": [
            {"label": "SQLAlchemy", "color": TAG_COLOR_REGISTRY["SQLAlchemy"]},
            {"label": "ORM", "color": TAG_COLOR_REGISTRY["ORM"]},
        ],
        "summary": {
            "goal": "Define relationships between SQLAlchemy models",
            "syllabus": [
                "One-to-many relationships",
                "Many-to-many relationships",
                "One-to-one relationships",
                "Backref and back_populates",
                "Cascade operations",
            ],
            "requirements": ["SQLAlchemy Models"],
        },
    },
    {
        "name": "Database Design",
        "description": "Design normalized database schemas",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Design efficient and normalized database schemas",
            "syllabus": [
                "Database normalization",
                "Primary and foreign keys",
                "Indexes",
                "Constraints",
                "Schema design patterns",
            ],
            "requirements": ["SQL Fundamentals"],
        },
    },
    {
        "name": "Many To Many",
        "description": "Implement many-to-many relationships",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
            {"label": "ORM", "color": TAG_COLOR_REGISTRY["ORM"]},
        ],
        "summary": {
            "goal": "Implement and query many-to-many relationships",
            "syllabus": [
                "Junction tables",
                "Many-to-many in SQL",
                "Many-to-many in ORMs",
                "Querying related data",
                "Additional fields in junction tables",
            ],
            "requirements": ["SQL Joins Mastery"],
        },
    },
    {
        "name": "Query Optimization",
        "description": "Optimize SQL queries for performance",
        "tags": [
            {"label": "SQL", "color": TAG_COLOR_REGISTRY["SQL"]},
        ],
        "summary": {
            "goal": "Optimize database queries for better performance",
            "syllabus": [
                "Query execution plans",
                "Index optimization",
                "Query refactoring",
                "Avoiding N+1 queries",
                "Caching strategies",
            ],
            "requirements": ["SQL Joins Mastery", "SQL Aggregations"],
        },
    },
]

GIT_COURSES = [
    {
        "name": "Git Basics",
        "description": "Version control fundamentals with Git",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "CLI", "color": TAG_COLOR_REGISTRY["CLI"]},
        ],
        "summary": {
            "goal": "Master Git basics for version control",
            "syllabus": [
                "What is version control?",
                "Git setup and configuration",
                "Creating repositories",
                "Commits and commit messages",
                "Git status and log",
            ],
            "requirements": [],
        },
    },
    {
        "name": "Branching Strategies",
        "description": "Git branching and merging strategies",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "CLI", "color": TAG_COLOR_REGISTRY["CLI"]},
        ],
        "summary": {
            "goal": "Master Git branching and merging workflows",
            "syllabus": [
                "Creating and switching branches",
                "Merging branches",
                "Branch naming conventions",
                "Feature branch workflow",
                "Gitflow workflow",
            ],
            "requirements": ["Git Basics"],
        },
    },
    {
        "name": "GitHub Pull Requests",
        "description": "Collaborate with pull requests",
        "tags": [
            {"label": "GitHub", "color": TAG_COLOR_REGISTRY["GitHub"]},
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
        ],
        "summary": {
            "goal": "Collaborate effectively using GitHub pull requests",
            "syllabus": [
                "Creating pull requests",
                "Code review process",
                "Commenting on PRs",
                "Merging strategies",
                "PR templates",
            ],
            "requirements": ["Branching Strategies"],
        },
    },
    {
        "name": "Merge Conflicts",
        "description": "Resolve merge conflicts like a pro",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "CLI", "color": TAG_COLOR_REGISTRY["CLI"]},
        ],
        "summary": {
            "goal": "Confidently resolve merge conflicts",
            "syllabus": [
                "Understanding merge conflicts",
                "Conflict markers",
                "Resolving conflicts manually",
                "Using merge tools",
                "Preventing conflicts",
            ],
            "requirements": ["Branching Strategies"],
        },
    },
    {
        "name": "Interactive Rebase",
        "description": "Clean up commit history with rebase",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "CLI", "color": TAG_COLOR_REGISTRY["CLI"]},
        ],
        "summary": {
            "goal": "Master interactive rebase for clean commit history",
            "syllabus": [
                "Rebase vs merge",
                "Interactive rebase commands",
                "Squashing commits",
                "Reordering commits",
                "When not to rebase",
            ],
            "requirements": ["Branching Strategies"],
        },
    },
    {
        "name": "Git Tags Releases",
        "description": "Tag releases and manage versions",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "GitHub", "color": TAG_COLOR_REGISTRY["GitHub"]},
        ],
        "summary": {
            "goal": "Use Git tags for version management",
            "syllabus": [
                "Creating tags",
                "Annotated vs lightweight tags",
                "Semantic versioning",
                "GitHub releases",
                "Release workflows",
            ],
            "requirements": ["Git Basics"],
        },
    },
    {
        "name": "Team Git Workflow",
        "description": "Git workflows for teams",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "GitHub", "color": TAG_COLOR_REGISTRY["GitHub"]},
        ],
        "summary": {
            "goal": "Implement effective Git workflows for teams",
            "syllabus": [
                "Centralized workflow",
                "Feature branch workflow",
                "Gitflow workflow",
                "Forking workflow",
                "Trunk-based development",
            ],
            "requirements": ["Branching Strategies", "GitHub Pull Requests"],
        },
    },
    {
        "name": "Git Hooks",
        "description": "Automate tasks with Git hooks",
        "tags": [
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
            {"label": "CLI", "color": TAG_COLOR_REGISTRY["CLI"]},
        ],
        "summary": {
            "goal": "Automate workflows using Git hooks",
            "syllabus": [
                "What are Git hooks?",
                "Client-side hooks",
                "Server-side hooks",
                "Common hook use cases",
                "Hook best practices",
            ],
            "requirements": ["Git Basics"],
        },
    },
    {
        "name": "Code Review Workflow",
        "description": "Effective code review practices",
        "tags": [
            {"label": "GitHub", "color": TAG_COLOR_REGISTRY["GitHub"]},
            {"label": "Git", "color": TAG_COLOR_REGISTRY["Git"]},
        ],
        "summary": {
            "goal": "Conduct effective code reviews",
            "syllabus": [
                "Code review principles",
                "What to look for",
                "Giving constructive feedback",
                "Receiving feedback",
                "Code review tools",
            ],
            "requirements": ["GitHub Pull Requests"],
        },
    },
    {
        "name": "GitHub Projects",
        "description": "Project management with GitHub",
        "tags": [
            {"label": "GitHub", "color": TAG_COLOR_REGISTRY["GitHub"]},
        ],
        "summary": {
            "goal": "Manage projects using GitHub Projects",
            "syllabus": [
                "Creating project boards",
                "Issues and milestones",
                "Automation",
                "Project views",
                "Team collaboration",
            ],
            "requirements": [],
        },
    },
]

BLOG_TITLES = [
    "Mastering React Hooks",
    "CSS Grid Tutorial",
    "REST API Best Practices",
    "Git Workflow Tips",
    "Database Design Patterns",
    "JavaScript Performance Tips",
    "Authentication Security Guide",
    "Flask Blueprint Strategies",
    "Responsive Design Techniques",
    "SQL Query Optimization",
    "React State Management",
    "Node.js Error Handling",
    "Modern CSS Features",
    "API Documentation Tips",
    "PostgreSQL Advanced Queries",
    "Frontend Testing Strategies",
    "Django Model Relationships",
    "Version Control Mastery",
    "Web Accessibility Guide",
    "Python Decorators Explained",
    "Tailwind CSS Tricks",
    "Express Middleware Patterns",
    "Database Migration Strategies",
    "GitHub Actions Workflows",
    "React Component Patterns",
    "SQLAlchemy Best Practices",
    "Backend Security Tips",
    "Git Rebase Guide",
    "Frontend Build Tools",
    "API Rate Limiting",
]


def image_for(name: str, topic: str) -> tuple[str, str]:
    url = "https://placehold.co/400x300"
    alt = f"{topic.capitalize()} course – {name}"
    return url, alt


def build_tags_for_blog(title: str) -> list[dict[str, str]]:
    """Build tags based on blog title keywords"""
    title_lower = title.lower()
    tags = []

    for tag, color in TAG_COLOR_REGISTRY.items():
        if tag.lower() in title_lower:
            tags.append({"label": tag, "color": color})

    if not tags:
        all_tags = list(TAG_COLOR_REGISTRY.items())
        selected = random.sample(all_tags, k=random.randint(2, 3))
        tags = [{"label": label, "color": color} for label, color in selected]

    return tags


def resolve_requirements(course_data, topic):
    """Convert requirement names to course IDs"""
    if not course_data.get("summary") or not course_data["summary"].get("requirements"):
        return course_data

    requirement_names = course_data["summary"]["requirements"]
    requirement_ids = []

    for req_name in requirement_names:
        req_course = Course.query.filter_by(name=req_name, topic=topic).first()
        if req_course:
            requirement_ids.append(req_course.id)

    # Update the requirements to use IDs instead of names
    course_data["summary"]["requirements"] = requirement_ids
    return course_data


def seed_courses(courses_data, topic):
    """Seed courses for a specific topic"""
    # First pass: create all courses without requirements
    for course_data in courses_data:
        course = Course.query.filter_by(name=course_data["name"]).first()
        if not course:
            img_url, img_alt = image_for(course_data["name"], topic)

            # Temporarily set requirements to empty for initial creation
            summary = course_data.get("summary")
            if summary and "requirements" in summary:
                temp_summary = summary.copy()
                temp_summary["requirements"] = []
            else:
                temp_summary = summary

            db.session.add(
                Course(
                    name=course_data["name"],
                    description=course_data["description"],
                    price=Decimal(str(round(random.uniform(4.99, 9.99), 2))),
                    discount=Decimal(str(round(random.uniform(0, 40), 2))),
                    topic=topic,
                    level=random.choice(["Beginner", "Intermediate", "Advanced"]),
                    tags=course_data.get("tags", []),
                    summary=temp_summary,
                    image_url=img_url,
                    image_alt=img_alt,
                )
            )

    db.session.commit()

    # Second pass: update requirements with actual IDs
    for course_data in courses_data:
        course = Course.query.filter_by(name=course_data["name"], topic=topic).first()
        if (
            course
            and course_data.get("summary")
            and "requirements" in course_data["summary"]
        ):
            requirement_names = course_data["summary"]["requirements"]
            requirement_ids = []

            for req_name in requirement_names:
                req_course = Course.query.filter_by(name=req_name, topic=topic).first()
                if req_course:
                    requirement_ids.append(req_course.id)

            # Update the course with resolved requirement IDs
            if course.summary:
                course.summary["requirements"] = requirement_ids

    db.session.commit()


with app.app_context():
    print("Seeding database...")

    # Seed all courses
    seed_courses(FRONTEND_COURSES, "frontend")
    seed_courses(BACKEND_COURSES, "backend")
    seed_courses(DATABASE_COURSES, "database")
    seed_courses(GIT_COURSES, "git")

    db.session.commit()

    # Seed 30 Blogs
    print("Seeding blogs...")
    for i in range(30):
        title = BLOG_TITLES[i]
        email = fake.unique.email()
        existing_blog = Blog.query.filter_by(title=title).first()

        if not existing_blog:
            db.session.add(
                Blog(
                    title=title,
                    author_name=fake.name(),
                    email=email,
                    url=fake.url(),
                    description=fake.sentence(nb_words=10),
                    tags=build_tags_for_blog(title),
                    image_url="https://placehold.co/400x300",
                    image_alt=f"Blog post - {title}",
                )
            )

    db.session.commit()

    # Get all IDs for user relationships
    all_course_ids = [course.id for course in Course.query.all()]
    all_blog_ids = [blog.id for blog in Blog.query.all()]

    # Seed 30 Users
    print("Seeding users...")
    for _ in range(30):
        username = fake.unique.user_name()
        email = fake.unique.email()
        existing_user = User.query.filter_by(email=email).first()

        if not existing_user:
            owned_courses = random.sample(
                all_course_ids, k=random.randint(1, min(10, len(all_course_ids)))
            )
            favourite_courses = random.sample(
                all_course_ids, k=random.randint(1, min(6, len(all_course_ids)))
            )
            saved_blogs = random.sample(
                all_blog_ids, k=random.randint(1, min(12, len(all_blog_ids)))
            )

            db.session.add(
                User(
                    username=username,
                    email=email,
                    password_hash=generate_password_hash("password123"),
                    owned_courses=owned_courses,
                    favourite_courses=favourite_courses,
                    saved_blogs=saved_blogs,
                )
            )

    db.session.commit()

    # Create permanent admin user using environment variables
    admin_username = os.getenv("ADMIN_USERNAME", "admin")
    admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
    admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

    admin_user = User.query.filter_by(email=admin_email).first()

    if not admin_user:
        print(f"Creating admin user ({admin_email})...")
        db.session.add(
            User(
                username=admin_username,
                email=admin_email,
                password_hash=generate_password_hash(admin_password),
                role="admin",
                owned_courses=all_course_ids,  # Admin owns all courses
                favourite_courses=[],
                saved_blogs=[],
            )
        )
        db.session.commit()
        print(f"✓ Admin user created ({admin_email})")
    else:
        print("✓ Admin user already exists")

    print("✓ Done. Seeded 40 courses, 30 blogs, and 30 users.")
