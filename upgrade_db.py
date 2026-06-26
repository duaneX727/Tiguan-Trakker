import sqlite3
import os

DB_FILE = "data/tiguan_data.db"

# Safety verification
if not os.path.exists(DB_FILE):
    print(f"❌ Database file not found at: {DB_FILE}")
    exit(1)

conn = sqlite3.connect(DB_FILE)
cursor = conn.cursor()

# Dictionary of all columns we need to add along with data types
columns_to_add = {
    "trip_distance": "REAL",
    "total_cost": "REAL",
    "mpg": "REAL",
    "notes": "TEXT"
}

print("🛠️ Initiating Python database upgrade sequence...")

for name, data_type in columns_to_add.items():
    try:
        cursor.execute(f"ALTER TABLE fuel_logs ADD COLUMN {name} {data_type};")
        print(f"✅ Column created successfully: {name} ({data_type})")
    except sqlite3.OperationalError as err:
        if "duplicate column name" in str(err):
            print(f"ℹ️ Skip: Column '{name}' is already tracked.")
        else:
            print(f"❌ Migration Error on column '{name}': {str(err)}")

conn.commit()
conn.close()
print("🎉 Schema structural update completed successfully!")