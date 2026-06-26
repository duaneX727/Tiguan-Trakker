import sqlite3
import os

db_path = os.path.join('data', 'fuel_log.db')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

try:
    cursor.execute("ALTER TABLE fuel_entries ADD COLUMN trip REAL;")
    conn.commit()
    print("Successfully added 'trip' column to database.")
except sqlite3.OperationalError as e:
    print(f"Error (column likely already exists): {e}")

conn.close()