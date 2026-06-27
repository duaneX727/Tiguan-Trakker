import sqlite3
import os

DB_FILE = "data/tiguan_data.db"

def run_analytics():
    if not os.path.exists(DB_FILE):
        print(f"❌ Error: Database file not found at {DB_FILE}")
        return

    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()

    # 1. Calculate Lifetime Metrics
    cursor.execute("""
        SELECT 
            COUNT(*), 
            SUM(gallons), 
            SUM(cost), 
            AVG(mpg) 
        FROM fuel_logs
    """)
    total_entries, total_gallons, total_cost, avg_mpg = cursor.fetchone()

    if not total_entries or total_entries == 0:
        print("ℹ️ The database is currently empty. Ingest some logs first!")
        conn.close()
        return

    print("\n==================================================")
    print("🚗 VOLKSWAGEN TIGUAN - LIFETIME ANALYTICS CRUISE 🚗")
    print("==================================================")
    print(f"📈 Total Fuel Logs Processed : {total_entries}")
    print(f"⛽ Total Gallons Pumped      : {total_gallons:.2f} Gal")
    print(f"💰 Total Financial Investment: ${total_cost:.2f}")
    print(f"🏁 Calculated Lifetime MPG   : {avg_mpg:.2f} MPG")
    print("==================================================\n")

    # 2. Fetch Latest 5 Entries
    print("📅 LATEST 5 FUEL LOG ENTRIES:")
    print(f"{'Date':<12} | {'Odometer':<10} | {'Trip (Mi)':<9} | {'Gallons':<8} | {'Cost':<7} | {'MPG':<5}")
    print("-" * 68)

    cursor.execute("""
        SELECT date, odometer, trip, gallons, cost, mpg 
        FROM fuel_logs 
        ORDER BY date DESC, rowid DESC 
        LIMIT 5
    """)
    rows = cursor.fetchall()

    for row in rows:
        date_str, odo, trip, gal, cost, mpg = row
        
        # Format variables cleanly to standard strings first
        odo_val  = f"{odo:.1f}" if odo is not None else "N/A"
        trip_val = f"{trip:.1f}" if trip is not None else "N/A"
        gal_val  = f"{gal:.2f}" if gal is not None else "N/A"
        cost_val = f"${cost:.2f}" if cost is not None else "N/A"
        mpg_val  = f"{mpg:.2f}" if mpg is not None else "N/A"
        
        print(f"{date_str:<12} | {odo_val:<10} | {trip_val:<9} | {gal_val:<8} | {cost_val:<7} | {mpg_val:<5}")
    
    print("==================================================\n")
    conn.close()

if __name__ == "__main__":
    run_analytics()
