import sqlite3

db_path = r"C:\Users\Motunrayo\Pycharm\ai_study_assistant\templates\study.db"

conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""")

print("Tables:")
print(c.fetchall())

conn.close()