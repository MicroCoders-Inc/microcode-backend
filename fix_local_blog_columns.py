"""
One-time script to fix the swapped blog columns in local SQLite database.
Run this once to fix your local development database.
"""

import sqlite3

def fix_blog_columns():
    """Swap blog columns to correct mapping."""
    conn = sqlite3.connect('instance/main.db')
    cursor = conn.cursor()

    try:
        print("Fixing blog column mapping in local database...")

        # Get all blogs with current (wrong) data
        cursor.execute("""
            SELECT id, content, image_url, image_alt
            FROM blog
        """)
        blogs = cursor.fetchall()

        print(f"Found {len(blogs)} blogs to fix")

        # Update each blog with corrected column mapping
        for blog_id, old_content, old_image_url, old_image_alt in blogs:
            # Swap: content->image_url, image_url->image_alt, image_alt->content
            cursor.execute("""
                UPDATE blog
                SET
                    content = ?,
                    image_url = ?,
                    image_alt = ?
                WHERE id = ?
            """, (old_image_alt, old_content, old_image_url, blog_id))

            print(f"  ✓ Fixed blog {blog_id}")

        conn.commit()
        print("\n✓ All blog columns fixed!")
        print("\nNow:")
        print("  - content = long article text")
        print("  - image_url = image URL")
        print("  - image_alt = short description")

    except Exception as e:
        print(f"✗ Error: {e}")
        conn.rollback()
        raise
    finally:
        conn.close()

if __name__ == '__main__':
    response = input("This will fix blog columns in instance/main.db. Proceed? (yes/no): ")
    if response.lower() == 'yes':
        fix_blog_columns()
    else:
        print("Cancelled.")
