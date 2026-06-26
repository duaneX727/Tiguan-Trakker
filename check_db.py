import sqlite3
import os

# Define the absolute path to your database
db_path = os.path.join(os.path.dirname(__file__), 'data', 'fuel_log.db')

def inspect_database():
    if not os.path.exists(db_path):
        print(f"Error: Database not found at {db_path}")
        return

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # 1. Print Table Schema
    print("--- Table Schema ---")
    cursor.execute("PRAGMA table_info(fuel_entries);")
    columns = cursor.fetchall()
    for col in columns:
        print(f"Column: {col[1]} (Type: {col[2]})")

    # 2. Fetch and Print all entries
    print("\n--- All Database Entries ---")
    cursor.execute("SELECT * FROM fuel_entries ORDER BY date DESC;")
    rows = cursor.fetchall()
    
    if not rows:
        print("No entries found.")
    else:
        for row in rows:
            print(row)

    conn.close()

if __name__ == "__main__":
    inspect_database()