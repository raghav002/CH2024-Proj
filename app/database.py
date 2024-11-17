import sqlite3

DB_PATH = "courses.db"

def get_connection():
    """Returns a connection to the database."""
    return sqlite3.connect(DB_PATH)

def create_tables():
    """Creates necessary tables for the application."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS courses (
        course_code TEXT PRIMARY KEY,
        title TEXT,
        description TEXT,
        credits INTEGER,
        prerequisites TEXT
      )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS requirements (
        major TEXT,
        category TEXT,
        required_courses TEXT,
        credits_needed INTEGER
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS feedback (
        user_id TEXT,
        course_code TEXT,
        feedback INTEGER
    )
    """)

    conn.commit()
    conn.close()
