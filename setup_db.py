import sqlite3

def init_db():
    # This creates the file if it doesn't exist
    conn = sqlite3.connect('/home/workdir/artifacts/fuel_log.db')
    cursor = conn.cursor()
    
    # Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS fuel_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            odometer REAL NOT NULL,
            gallons REAL NOT NULL,
            price_per_gallon REAL NOT NULL,
            total_cost REAL NOT NULL
        )
    ''')
    
    conn.commit()
    conn.close()
    print("Database initialized successfully at /home/workdir/artifacts/fuel_log.db")

if __name__ == "__main__":
    init_db()