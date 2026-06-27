import sqlite3
import os
import re

DB_FILE = "data/tiguan_data.db"
CSV_FILE = "data/raw_logs.csv"

def clean_to_float(text):
    if not text:
        return None
    # Strip away dollar signs, commas, asterisks, and terminal garbage
    cleaned = text.replace('$', '').replace(',', '').replace('*', '').strip()
    # Check if it's a dash indicator or placeholder text
    if not cleaned or any(d in cleaned for d in ['—', '–', '-', 'â€“', 'N/A']):
        return None
    try:
        return float(cleaned)
    except ValueError:
        return None

def batch_load():
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: Cannot find your data log sheet at {CSV_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    print("🧹 Wiping database for a clean, verified reload...")
    cursor.execute("DELETE FROM fuel_logs")
    
    print(f"📖 Reading real logs from {CSV_FILE}...")
    with open(CSV_FILE, mode='r', encoding='utf-8') as f:
        lines = f.readlines()
        
    inserted_count = 0
    
    for index, line in enumerate(lines):
        line_clean = line.strip()
        if not line_clean or index == 0 or "Date" in line_clean:
            continue
            
        # Split purely by whitespace columns
        parts = line_clean.split()
        if len(parts) < 4:
            continue
            
        try:
            # 1. Date is always the first column item
            date_raw = parts[0]
            date_str = f"{date_raw}, 2026" if "," not in date_raw else date_raw
            
            # 2. Odometer is always the second column item
            odometer = clean_to_float(parts[1])
            
            # 3. Dynamically unpack the metrics loop following the Odometer
            remaining_tokens = parts[2:]
            
            # Filter out any lingering dash rows from our numbers pool
            numeric_values = []
            has_dash_in_trip = False
            
            for i, token in enumerate(remaining_tokens):
                # Identify if the very first token after odometer is a dash (missing trip)
                if i == 0 and any(d in token for d in ['—', '–', '-', 'â€“']):
                    has_dash_in_trip = True
                
                val = clean_to_float(token)
                if val is not None:
                    numeric_values = numeric_values + [val]
            
            # Match assignments depending on whether trip was empty/dashed
            if has_dash_in_trip or len(numeric_values) == 3:
                trip_distance = None
                gallons       = numeric_values[0]
                total_cost    = numeric_values[1]
            elif len(numeric_values) >= 4:
                trip_distance = numeric_values[0]
                gallons       = numeric_values[1]
                total_cost    = numeric_values[2]
            else:
                continue

            # Skip lines where parsing completely missed required values
            if odometer is None or gallons is None or total_cost is None:
                continue

            mpg = (trip_distance / gallons) if (trip_distance and gallons) else None
            notes = ""

            cursor.execute("""
                INSERT INTO fuel_logs (
                    date, odometer, trip, gallons, cost, notes, mpg
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (date_str, odometer, trip_distance, gallons, total_cost, notes, mpg))
            inserted_count += 1
            
        except Exception:
            continue

    conn.commit()
    conn.close()
    print(f"✅ Success! Ingested {inserted_count} clean log rows.")

if __name__ == "__main__":
    batch_load()
