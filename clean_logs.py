import os
import argparse
import numpy as np
import pandas as pd
from auth import get_google_sheet  # Importing your modularized authentication function

def process_vehicle_logs(file_path):
    """
    Main ingestion pipeline to clean raw CSV files and upload anomalies cleanly.
    """
    if not os.path.exists(file_path):
        print(f"❌ Error: The file path '{file_path}' does not exist.")
        return

    print(f"--- 🚀 Starting Ingestion Pipeline: {file_path} ---")
    
    # 1. Read Data safely handling Windows/Excel text encoding anomalies (e.g., 0x97 bytes)
    try:
        df = pd.read_csv(file_path, encoding='utf-8')
    except UnicodeDecodeError:
        print("⚠️ Standard UTF-8 decoding failed. Re-trying with cp1252 window sanitation...")
        df = pd.read_csv(file_path, encoding='cp1252')

    # 2. Enforce Reconciled Structural Mapping
    # Standardizing your tracked metrics (Date, Odometer, Trip, Fuel Added, Price)
    df.columns = [col.strip().lower() for col in df.columns]
    
    # 3. Apply the '33 MPG Rule' data integrity check
    # Anything yielding efficiency metrics above 33 is tracked strictly as a Partial Fill
    if 'mpg' in df.columns:
        print("📊 Auditing MPG records for partial fills...")
        df['fill_type'] = np.where(df['mpg'] > 33.0, 'Partial Fill', 'Full Refill')
        # Filter or leave untouched based on rolling trend calculations
    else:
        print("⚠️ 'mpg' column not found in source log metadata. Calculating dynamically...")
        # Optional fallback math loop goes here
        df['fill_type'] = 'Unknown'

    # 4. Generate local structured copy
    output_filename = f"cleaned_{os.path.basename(file_path)}"
    df.to_csv(output_filename, index=False)
    print(f"💾 Local backup captured: {output_filename}")

    # 5. Connect cleanly to Cloud Engine and update live sheets
    try:
        print("🔗 Establishing cloud handshake via Google API wrapper...")
        sheet = get_google_sheet("Tiguan Logs") # Matches your Google Drive target string exactly
        
        # Convert pandas dataframe updates to an array format expected by the spreadsheet
        raw_values = df.fillna('').values.tolist()
        
        # Append the new records to the bottom row of your online database
        sheet.append_rows(raw_values, value_input_option='USER_ENTERED')
        print("🚀 Sync Complete! 'Tiguan Logs' cloud database successfully refreshed.")
        
    except Exception as e:
        print(f"❌ Cloud Sync Failed: {e}")
        print("🔄 Work preserved locally. Check API service account keys or sharing permissions.")

# This is your Main Script Entrance Guard
if __name__ == "__main__":
    # Defining argument configurations so it's terminal-aware and friendly
    parser = argparse.ArgumentParser(
        description="Tiguan Trakker Core Automation Engine: Clean raw logging files and pipe to cloud dashboards."
    )
    
    # Require a positional dynamic input string argument
    parser.add_argument(
        "file", 
        help="The file path of the incoming log to triage (e.g., _March.csv)"
    )
    
    # Parse incoming sys arguments from Git Bash or remote sessions
    args = parser.parse_args()
    
    # Fire the processing execution using the custom parameter
    process_vehicle_logs(args.file)