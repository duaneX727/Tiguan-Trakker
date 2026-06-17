import sqlite3

def run_smoke_test():
    # Create an in-memory database for testing (no file created)
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()
    
    # 1. Test Schema Creation
    cursor.execute('''CREATE TABLE fuel_entries (odometer REAL, gallons REAL)''')
    
    # 2. Test Data Insertion
    cursor.execute("INSERT INTO fuel_entries VALUES (15000.5, 12.0)")
    
    # 3. Test Retrieval
    cursor.execute("SELECT * FROM fuel_entries")
    result = cursor.fetchone()
    
    assert result == (15000.5, 12.0), "Data mismatch in test!"
    print("Test passed: Database schema and basic I/O are working.")
    conn.close()

if __name__ == "__main__":
    run_smoke_test()