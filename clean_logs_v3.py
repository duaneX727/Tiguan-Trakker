"""
Project: Tiguan Trakker
Version: 3.0
Changes: Added duplicate handling and flexible date parsing.
Auth: Integrated with auth.py via GitHub/Service Account
"""

import pandas as pd
import numpy as np
import argparse
import os


def process_vehicle_logs(input_file):
    # 1. Define the columns to maximize field capture
    column_names = ["Date", "Odometer", "Trip", "Fuel_Type", "Gallons", "Cost", "MPG", "Status", "Note_1", "Note_2"]
    
    # 2. Load the raw data using those names
    try:
        df = pd.read_csv(input_file, names=column_names, header=None, engine='python', on_bad_lines='skip')
    except Exception as e:
        print(f"Error reading file: {e}")
        return None
    # ... rest of your cleaning logic ...
   

    # 2. Apply your specific logic rules
    # Odometer is currently around 111,562
    # Rule: 
    # 
    # If MPG > 33, it's a partial fill -> set MPG to NaN or Note
    # Refined Logic
    # Use np.where to switch values based on your 33 MPG rule
    if 'MPG' in df.columns:
        df['MPG'] = pd.to_numeric(df['MPG'], errors='coerce')
        
        # Rule: If MPG > 33, it's a partial fill. 
        # We create a 'Fill_Type' column to track this without losing the actual MPG number.
        df['Fill_Type'] = np.where(df['MPG'] > 33, 'Partial', 'Full')
        # Keep the MPG but you now know which ones to trust for averages!
        
        # Optional: df.loc[df['MPG'] > 33, 'MPG'] = None # Uncomment to wipe partial MPG values

    # 3. Generate Output Filename
    output_file = f"cleaned_{os.path.basename(input_file)}"
    
    # 4. Save the processed data
    # A. Convert dates to a uniform format (YYYY-MM-DD)
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=False, errors='coerce').dt.strftime('%Y-%m-%d')

    # B. Remove duplicates based on Date and Odometer
    df = df.drop_duplicates(subset=['Date', 'Odometer'], keep='first')

    # C. Sort by Odometer so the math always flows forward
    df = df.sort_values('Odometer')
    df.to_csv(output_file, index=False)
    print(f"Success! Cleaned data saved to: {output_file}")
    return df # Make sure your process function returns the dataframe!

def blind_append_to_sheets(df, spreadsheet_name, worksheet_name):
        try:
           import auth  # Leveraging your successful auth.py
           client = auth.get_gspread_client() # Or whatever your auth function is named
        
        # Open the sheet
           sh = client.open(spreadsheet_name)
           worksheet = sh.worksheet(worksheet_name)
        
        # Convert DataFrame to a list of lists (handling NaNs for Google Sheets)
        # Sheets doesn't like 'NaN', so we fill them with empty strings
           upload_data = df.fillna('').values.tolist()
        
        # Perform the append
           worksheet.append_rows(upload_data, value_input_option='USER_ENTERED')
           print(f"🚀 Success! {len(upload_data)} rows appended to {worksheet_name}.")
        
        except Exception as e:
           print(f"❌ Sync failed: {e}")
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tiguan Trakker")
    parser.add_argument("file", help="The name of the raw CSV file to process")
    args = parser.parse_args()

    # 1. This runs the cleaning and gets the "cleaned_df" back
    cleaned_df = process_vehicle_logs(args.file)

    if cleaned_df is not None:
        # 2. Trigger the sync using the dataframe we just cleaned
        confirm = input("\nData cleaned locally. Ready to sync to Google Sheets? (y/n): ")
        if confirm.lower() == 'y':
            # Add the names of your specific Google Sheet and the Tab
            blind_append_to_sheets(cleaned_df, "Tiguan_Master_Log", "Sheet1")
        else:
            print("Sync cancelled. Local file is available for review.")