import csv
import sqlite3
import os

DB_FILE = "data/tiguan_data.db"
CSV_FILE = "data/raw_logs.csv"

def batch_load():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: Cannot find your data log sheet at {CSV_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Purge all the stale test placeholders cleanly first
    print("🧹 Purging old 1970 placeholder rows from database...")
    cursor.execute("DELETE FROM fuel_logs WHERE date LIKE '1970%'")
    
    # 2. Open and parse the CSV spreadsheet rows
    print(f"📖 Reading real logs from {CSV_FILE}...")
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        # Detects if your spreadsheet uses a header row
        sample = f.read(2048)
        has_header = csv.Sniffer().has_header(sample) if sample else False
        f.seek(0)
        
        reader = csv.reader(f)
        if has_header:
            next(reader) # Skip header titles line safely
            
        inserted_count = 0
        for row in reader:
            if not row or len(row) < 5:
                continue # Skip empty lines
                
            # Extract standard positional fields matching your data columns
            # Adjust mapping safely if your CSV structure differs
            date_str = row[0].strip()
            try:
                odometer = float(row[1])
                trip_distance = float(row[2]) if row[2] else None
                gallons = float(row[3])
                total_cost = float(row[4])
                notes = row[5].strip() if len(row) > 5 else ""
                
                # Calculate metric on the fly if missing from row cells
                mpg = (trip_distance / gallons) if (trip_distance and gallons) else None
            except ValueError:
                continue # Skip malformed numeric lines cleanly

            cursor.execute("""
                INSERT INTO fuel_logs (
                    date, odometer, trip, gallons, cost, notes, mpg
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date_str, odometer, trip_distance, gallons, total_cost, notes, mpg))
            inserted_count += 1

    conn.commit()
    conn.close()
    print(f"✅ Success! Ingested {inserted_count} official log rows into your production database.")

if __name__ == "__main__":
    batch_load()