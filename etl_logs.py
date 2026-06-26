import os
import json
import sqlite3
import sys
from datetime import datetime

# =====================================================================
# CONFIGURATION
# =====================================================================
# Path where the Node.js webhook server drops the payload file
DATA_FILE = "latest_fuel_log.json"

# Absolute or relative path to your verified SQLite database file
DB_FILE = "data/tiguan_data.db"


def calculate_metrics(trip_distance, gallons, total_cost):
    """
    Calculates derived metrics for the database entries.
    Handles division-by-zero safety checks cleanly.
    """
    mpg = 0.0
    calculated_cpg = 0.0

    if gallons > 0:
        mpg = round(trip_distance / gallons, 2)
        calculated_cpg = round(total_cost / gallons, 3)

    return mpg, calculated_cpg


def process_webhook_payload():
    print("=====================================================")
    print(f"⏰ Execution Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=====================================================")

    # 1. Verification Check: Ensure the payload file exists
    if not os.path.exists(DATA_FILE):
        print(f"ℹ️ No fresh webhook payload file found at '{DATA_FILE}'.")
        print("   Standing by for the next mobile ingestion event...")
        return False

    print(f"📂 Found fresh webhook payload file: {DATA_FILE}")

    try:
        # 2. Read and parse the structured data payload natively
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            log_data = json.load(f)

        # 3. Data Extraction & Direct Type Casting
        date_str = log_data.get('date', datetime.now().strftime('%Y-%m-%d'))
        odometer = float(log_data.get('odometer', 0))
        trip_distance = float(log_data.get('trip_distance', 0))
        gallons = float(log_data.get('gallons', 0))
        price_per_gallon = float(log_data.get('price_per_gallon', 0))
        total_cost = float(log_data.get('total_cost', 0))
        notes = log_data.get('notes', '').strip()

        print(f"📱 Data Successfully Parsed:")
        print(f"   Date: {date_str} | Odo: {odometer} | Trip: {trip_distance} mi")
        print(f"   Gallons: {gallons} | Price/Gal: ${price_per_gallon} | Total: ${total_cost}")

        # 4. Pipeline Enrichment: Calculate MPG and Cost Per Gallon
        mpg, calculated_cpg = calculate_metrics(trip_distance, gallons, total_cost)
        print(f"📊 Calculated Pipeline Metrics: MPG: {mpg} | Cost/Gal: ${calculated_cpg}")

        # 5. Database Injection: Bridge to local SQLite instance
        print(f"🗄️ Opening connection to database: {DB_FILE}")
        conn = sqlite3.connect(DB_FILE)
        cursor = conn.cursor()

        # Safely insert matching your exact database columns: date, odometer, trip, gallons, cost, notes, mpg
        cursor.execute("""
            INSERT INTO fuel_logs (
                date, 
                odometer, 
                trip, 
                gallons, 
                cost, 
                notes,
                mpg
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (date_str, odometer, trip_distance, gallons, total_cost, notes, mpg))

        conn.commit()
        conn.close()
        print("💾 Metrics successfully committed and indexed into SQLite binary.")

        # 6. Housekeeping: Safely evict the staging file to prevent duplicate processing
        os.remove(DATA_FILE)
        print(f"🧹 Cleaned up temporary pipeline file '{DATA_FILE}' safely.")
        print("=====================================================\n")
        return True

    except json.JSONDecodeError:
        print(f"❌ Critical Error: The payload file '{DATA_FILE}' contains malformed JSON markup.")
        return False
    except sqlite3.Error as db_err:
        print(f"❌ Database Engine Error during injection: {str(db_err)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected Error encountered in processing pipeline: {str(e)}")
        return False


if __name__ == "__main__":
    success = process_webhook_payload()
    # Return appropriate system exit status codes for shell runners
    if not success:
        sys.exit(1)
    sys.exit(0)
    