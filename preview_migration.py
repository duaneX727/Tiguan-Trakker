import sqlite3
import csv

def preview_migration():
    # 1. Setup temp DB
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE fuel_entries (date TEXT, odometer REAL, gallons REAL, price REAL)')
    
    # 2. Mock row from your CSV (replace with your actual CSV header/data format)
    # This assumes your CSV has columns like: date, odometer, gallons, price
    mock_row = ('2026-06-15', 15000.5, 12.0, 3.50)
    
    # 3. Insert and verify
    cursor.execute("INSERT INTO fuel_entries VALUES (?,?,?,?)", mock_row)
    cursor.execute("SELECT * FROM fuel_entries")
    print(f"Successfully migrated sample record: {cursor.fetchone()}")
    conn.close()

if __name__ == "__main__":
    preview_migration()