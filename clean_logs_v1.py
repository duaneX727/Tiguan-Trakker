import csv
import os

# The Master Header we agreed on
HEADERS = [
    "Date", "Odometer", "Trip", "FuelType", "Gallons", 
    "PriceGal", "TotalCost", "MPG", "OilLife_%", 
    "TirePressure_PSI", "ServiceFlag", "Notes"
]

def append_log_entry(data_dict):
    file_path = 'tiguan_logs.csv'
    # file_path = '_March.csv'
    # file_path =_
    # file_exists = os.path.isfile(file_path)
    # Check if entry already exists to prevent redundancy
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            if f"{data_dict['Date']},{data_dict['Odometer']}" in f.read():
                print(f"Skipping duplicate entry for {data_dict['Date']}")
                return

    # ... (the rest of your writing code below)
    with open(file_path, 'a', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists: # type: ignore
            writer.writeheader()
        
        # This ensures missing data stays blank
        row = {header: data_dict.get(header, "") for header in HEADERS}
        writer.writerow(row)
    print("Successfully added entry to K10 Master Log.")

# Example of how we will run it for your data:
# Copy and replace the 'new_entry' section with this:
entries = [
    
    {"Date": "2025-12-23", "Odometer": "91718", "Trip": "438.0", "FuelType": "Premium 93", "Gallons": "13.412", "PriceGal": "3.129", "TotalCost": "41.97"},
    {"Date": "2025-12-25", "Odometer": "92418", "Trip": "325.1", "FuelType": "Premium 93", "Gallons": "11.228"},
    {"Date": "2025-12-28", "Odometer": "93001", "Notes": "Current reading from app screenshot"}
]

for entry in entries:
    append_log_entry(entry)