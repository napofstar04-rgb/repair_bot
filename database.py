import sqlite3


def create_db():

    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS schedules (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            full_name TEXT,
            days TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY
        )
    """)
    conn.commit()
    conn.close()


def save_schedule(user_id, full_name, days):

    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO schedules (
            user_id,
            full_name,
            days
        )
        VALUES (?, ?, ?)
    """, (
        user_id,
        full_name,
        days
    ))

    conn.commit()
    conn.close()
def save_user(user_id):

    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO users (user_id)
        VALUES (?)
    """, (user_id,))

    conn.commit()
    conn.close()
def get_all_users():

    conn = sqlite3.connect("schedule.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT user_id FROM users
    """)

    users = cursor.fetchall()

    conn.close()

    return users