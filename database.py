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