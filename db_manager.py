import sqlite3
import csv
import os

# Configuration
DB_PATH = 'data/fuel_log.db'
CSV_PATH = 'archive/logs/tiguan_logs.csv'

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            odometer REAL,
            gallons REAL,
            price_per_gallon REAL
        )
    ''')
    conn.commit()
    conn.close()
    print(f"Database initialized at {DB_PATH}")

def import_csv_to_db():
    if not os.path.exists(CSV_PATH):
        print(f"Error: {CSV_PATH} not found.")
        return

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    with open(CSV_PATH, 'r') as f:
        reader = csv.reader(f)
        next(reader) # Skips header
        for row in reader:
            # Explicitly select only the 4 columns
            data_to_insert = (row[0], row[1], row[2], row[3])
            cursor.execute('''
                INSERT INTO fuel_entries (date, odometer, gallons, price_per_gallon) 
                VALUES (?, ?, ?, ?)
            ''', data_to_insert)
    
    conn.commit()
    conn.close()
    print("Migration successful.")

if __name__ == "__main__":
    init_db()
    import_csv_to_db()