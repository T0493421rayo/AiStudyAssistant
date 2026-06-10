import sqlite3

def init_db():
    conn = sqlite3.connect("study.db")
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS quizzes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        score INTEGER,
        total INTEGER,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )
    """)

    conn.commit()
    conn.close()