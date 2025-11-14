"""
Migration script to copy data from local SQLite database to Render PostgreSQL.

Usage:
    export RENDER_DATABASE_URL="postgresql://user:password@host/database"
    python migrate_to_postgres.py

Or:
    python migrate_to_postgres.py postgresql://user:password@host/database
"""

import os
import sys
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate, upgrade
from app.database import db
from app.models import User, Course, Blog, Contact, Purchase

def create_tables_in_target(target_db_url):
    """
    Create all tables in the target database by running migrations.

    Args:
        target_db_url: PostgreSQL database URL where tables will be created
    """
    print("Creating tables in target database...")
    print("Running migrations...\n")

    # Create a temporary Flask app with the target database
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = target_db_url
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize db and migrate with this app
    temp_db = SQLAlchemy(app)
    migrate = Migrate(app, temp_db)

    try:
        with app.app_context():
            # Run migrations to create all tables
            upgrade()
            print("✓ Tables created successfully\n")
    except Exception as e:
        print(f"✗ Error creating tables: {e}")
        print("\nNote: If this fails, make sure:")
        print("  1. The database exists and is accessible")
        print("  2. Your migrations folder is present")
        print("  3. You have run 'flask db migrate' locally first")
        raise

def migrate_data(source_db_url, target_db_url):
    """
    Migrate data from source database to target database.

    Args:
        source_db_url: SQLite database URL (e.g., 'sqlite:///instance/main.db')
        target_db_url: PostgreSQL database URL from Render
    """
    print(f"Source DB: {source_db_url}")
    print(f"Target DB: {target_db_url[:20]}...")  # Don't print full URL with password

    # Create engines
    source_engine = create_engine(source_db_url)
    target_engine = create_engine(target_db_url)

    # Create sessions
    SourceSession = sessionmaker(bind=source_engine)
    TargetSession = sessionmaker(bind=target_engine)

    source_session = SourceSession()
    target_session = TargetSession()

    try:
        # Define models to migrate in order (respecting foreign keys)
        models_to_migrate = [
            (User, 'Users'),
            (Course, 'Courses'),
            (Blog, 'Blogs'),
            (Contact, 'Contacts'),
            (Shop, 'Shop items'),
            (Article, 'Articles'),
            (Purchase, 'Purchases'),
        ]

        total_migrated = 0
        skipped_records = []

        # Track migrated IDs for foreign key validation
        migrated_user_ids = set()
        migrated_course_ids = set()

        for model, name in models_to_migrate:
            try:
                # Get all records from source
                records = source_session.query(model).all()
                count = len(records)

                if count == 0:
                    print(f"  {name}: No records to migrate")
                    continue

                print(f"  Migrating {count} {name}...", end=' ')

                # Convert to dicts and create new instances for target
                for record in records:
                    # Get the dict representation
                    record_dict = {}
                    for column in inspect(model).mapper.column_attrs:
                        record_dict[column.key] = getattr(record, column.key)

                    # Special handling for Blog model - fix column mapping
                    if model == Blog:
                        # SQLite has columns mixed up, fix the mapping:
                        # SQLite content -> PostgreSQL image_url
                        # SQLite image_url -> PostgreSQL image_alt
                        # SQLite image_alt -> PostgreSQL content
                        temp_content = record_dict.get('content')
                        temp_image_url = record_dict.get('image_url')
                        temp_image_alt = record_dict.get('image_alt')

                        record_dict['image_url'] = temp_content
                        record_dict['image_alt'] = temp_image_url
                        record_dict['content'] = temp_image_alt

                    # Special handling for Purchase model - validate foreign keys
                    if model == Purchase:
                        user_id = record_dict.get('user_id')
                        course_id = record_dict.get('course_id')

                        # Skip if references non-existent user or course
                        if user_id not in migrated_user_ids:
                            skipped_records.append(f"Purchase {record_dict.get('id')} (user {user_id} doesn't exist)")
                            continue
                        if course_id not in migrated_course_ids:
                            skipped_records.append(f"Purchase {record_dict.get('id')} (course {course_id} doesn't exist)")
                            continue

                    # Track migrated IDs
                    if model == User:
                        migrated_user_ids.add(record_dict.get('id'))
                    elif model == Course:
                        migrated_course_ids.add(record_dict.get('id'))

                    # Create new instance for target database
                    new_record = model(**record_dict)
                    target_session.add(new_record)

                target_session.commit()
                print(f"✓ Done")
                total_migrated += count

            except Exception as e:
                print(f"✗ Error: {e}")
                target_session.rollback()
                raise

        print(f"\n✓ Migration complete! Total records migrated: {total_migrated}")

        if skipped_records:
            print(f"\n⚠ Skipped {len(skipped_records)} records due to missing foreign keys:")
            for skip in skipped_records:
                print(f"  - {skip}")

    except Exception as e:
        print(f"\n✗ Migration failed: {e}")
        target_session.rollback()
        raise
    finally:
        source_session.close()
        target_session.close()


def main():
    """Main migration function."""
    # Get target database URL
    target_db_url = None

    if len(sys.argv) > 1:
        target_db_url = sys.argv[1]
    else:
        target_db_url = os.getenv('RENDER_DATABASE_URL')

    if not target_db_url:
        print("Error: Please provide PostgreSQL database URL")
        print("\nUsage:")
        print("  export RENDER_DATABASE_URL='postgresql://...'")
        print("  python migrate_to_postgres.py")
        print("\nOr:")
        print("  python migrate_to_postgres.py 'postgresql://...'")
        sys.exit(1)

    # Always use local SQLite database as source
    # Don't use DATABASE_URL from .env as it may be incorrect
    source_db_url = 'sqlite:///instance/main.db'

    # Confirm migration
    print("=" * 60)
    print("DATABASE MIGRATION")
    print("=" * 60)
    print(f"\nThis will copy all data from:")
    print(f"  LOCAL:  {source_db_url}")
    print(f"  TO:     {target_db_url[:30]}...")
    print("\nWARNING: This will ADD data to the target database.")
    print("Make sure the target database is empty or reset first!")
    print("=" * 60)

    response = input("\nProceed with migration? (yes/no): ")
    if response.lower() != 'yes':
        print("Migration cancelled.")
        sys.exit(0)

    print("\nStarting migration...\n")

    # Step 1: Create tables in target database
    try:
        create_tables_in_target(target_db_url)
    except Exception as e:
        print(f"\n✗ Failed to create tables: {e}")
        sys.exit(1)

    # Step 2: Migrate data
    migrate_data(source_db_url, target_db_url)


if __name__ == '__main__':
    main()
