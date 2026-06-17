import sqlite3

def verify_data():
    conn = sqlite3.connect('data/fuel_log.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM fuel_entries LIMIT 5")
    rows = cursor.fetchall()
    
    print("--- First 5 Entries in Database ---")
    for row in rows:
        print(row)
    
    conn.close()

if __name__ == "__main__":
    verify_data()