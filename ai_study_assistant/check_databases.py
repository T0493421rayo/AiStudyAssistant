import sqlite3
import os

DATABASE = r"C:\Users\Motunrayo\Pycharm\ai_study_assistant\study.db"

print("Database being checked:")
print(DATABASE)

conn = sqlite3.connect(DATABASE)
c = conn.cursor()

c.execute("""
    SELECT name
    FROM sqlite_master
    WHERE type='table'
""")

tables = c.fetchall()

print("\nTables:")
print(tables)

for table in tables:

    table_name = table[0]

    c.execute(
        f"SELECT COUNT(*) FROM [{table_name}]"
    )

    count = c.fetchone()[0]

    print(f"{table_name}: {count} rows")

conn.close()