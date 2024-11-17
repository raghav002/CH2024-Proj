from app.database import get_connection

def save_feedback(user_id, course_code, feedback):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO feedback (user_id, course_code, feedback)
    VALUES (?, ?, ?)
    """, (user_id, course_code, feedback))

    conn.commit()
    conn.close()
