import sqlite3
import csv
import os
import sys

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
            trip REAL,
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
        next(reader)  # Skips header
        for row in reader:
            # Assuming CSV columns are: date, odo, trip, gal, price
            cursor.execute('''
                INSERT INTO fuel_entries (date, odometer, trip, gallons, price_per_gallon)
                VALUES (?, ?, ?, ?, ?)
            ''', (row[0], row[1], row[2], row[3], row[4]))
    conn.commit()
    conn.close()
    print("Bulk migration successful.")

def add_single_entry(date, odo, trip, gal, price):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO fuel_entries (date, odometer, trip, gallons, price_per_gallon)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, odo, trip, gal, price))
    conn.commit()
    conn.close()
    print(f"Successfully added entry: {date} (Trip: {trip})")

def import_backlog(backlog_path):
    if not os.path.exists(backlog_path):
        print(f"Error: {backlog_path} not found.")
        return
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(backlog_path, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            cursor.execute('''
                INSERT INTO fuel_entries (date, odometer, trip, gallons, price_per_gallon)
                VALUES (?, ?, ?, ?, ?)
            ''', (row[0], row[1], row[2], row[3], row[4]))
    conn.commit()
    conn.close()
    print(f"Backlog migration from {backlog_path} completed.")

if __name__ == "__main__":
    if "--add" in sys.argv:
        # Usage: python db_manager.py --add [date] [odo] [trip] [gal] [price]
        add_single_entry(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    elif "--backlog" in sys.argv:
        # Usage: python db_manager.py --backlog [file_path]
        import_backlog(sys.argv[2])
    else:
        init_db()
        import_csv_to_db()