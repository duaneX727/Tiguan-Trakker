import csv
import os
import pandas as pd
import gspread
from auth import get_sheet  # Import your custom function

def process_and_upload(csv_file):
    # 1. Clean your logs
    df = pd.read_csv(csv_file)
    # ... (Your existing logic for filtering, etc.) ...
    
    # 2. Upload to Google Sheets
    sheet = get_sheet("Tiguan Logs")
    if sheet:
        # Convert dataframe to list of lists for gspread
        data = df.values.tolist()
        sheet.append_rows(data)
        print("Data successfully pushed to Google Sheets!")
    else:
        print("Failed to push data.")

# 1. CONFIGURATION
MASTER_FILE = "clean_logs.csv"
HEADERS = ["Date", "Odometer", "Trip", "FuelType", "Gallons", "Cost", "MPG", "Notes"]

# Mapping: "Old/Raw CSV Header": "New Master Header"
HEADER_MAP = {
    "Date": "Date",
    "Ending Odometer": "Odometer",
    "Miles Since Last Fill": "Trip",
    "Gas Expense": "Cost",
    "Fuel Type": "FuelType",
    "Gallons": "Gallons",
    "MPG": "MPG",
    "Notes": "Notes"
}

# 2. TRIAGE LOGIC
def triage_data(raw_dict):
    clean_dict = {}
    for old_key, new_key in HEADER_MAP.items():
        val = raw_dict.get(old_key, "")
        
        # Clean numeric strings (remove ' miles', commas, etc.)
        if isinstance(val, str):
            val = val.replace(" miles", "").replace(",", "").strip()
            
        clean_dict[new_key] = val
    
    # Auto-flag Partial Fills
    try:
        mpg_val = float(clean_dict.get("MPG", 0))
        if mpg_val > 33:
            clean_dict["MPG"] = "Partial"
            if not clean_dict["Notes"]:
                clean_dict["Notes"] = f"Partial fill (Calc: {mpg_val})"
    except (ValueError, TypeError):
        pass
        
    return clean_dict

# 3. APPEND LOGIC (With Duplicate Protection)
def append_log_entry(data_dict):
    file_exists = os.path.isfile(MASTER_FILE)
    
    # Duplicate Check (Date + Odometer)
    if file_exists:
        with open(MASTER_FILE, "r") as f:
            content = f.read()
            if f"{data_dict['Date']},{data_dict['Odometer']}" in content:
                print(f"   - Skipping: {data_dict['Date']} at {data_dict['Odometer']} (Already exists)")
                return

    with open(MASTER_FILE, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)
        if not file_exists:
            writer.writeheader()
        
        row = {h: data_dict.get(h, "") for h in HEADERS}
        writer.writerow(row)
        print(f"   + Logged: {data_dict['Date']} - {data_dict['Odometer']} mi")

# 4. FILE PROCESSING ENGINE (With Try/Except)
def process_raw_file(input_file_path):
    if not os.path.exists(input_file_path):
        print(f"ERROR: File '{input_file_path}' not found.")
        return

    print(f"--- Processing Raw File: {input_file_path} ---")
    try:
        with open(input_file_path, mode='r', encoding='latin-1') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                try:
                    clean = triage_data(row)
                    # Only append if there is actual data (at least a Date and Odometer)
                    if clean["Date"] and clean["Odometer"]:
                        append_log_entry(clean)
                except Exception as row_err:
                    print(f"   ! Error on specific row: {row_err}")

        print(f"--- Finished '{input_file_path}' ---")

    except PermissionError:
        print(f"ERROR: '{input_file_path}' is open in another app. Close it and retry.")
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")

# 5. EXECUTION (The "Next Move" Zone)
if __name__ == "__main__":
    # To process a file, just update the filename here:
    process_raw_file("_March.csv")
    
    # Tip: You can even run multiple files at once:
    # process_raw_file("_April_Backlog.csv")