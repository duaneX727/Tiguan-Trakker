import sys
import gspread
import auth  # Assumes your auth.py is in the same folder

# --- CONFIGURATION: MASTER SCHEMA ---
# This is our locked-in header list for the Google Sheet
TIGUAN_HEADERS = [
    "Date", "Odometer", "Trip", "Fuel_Type", "Gallons", 
    "Price_Per_Gal", "Total_Cost", "Calc_MPG", 
    "Tire_Pressure", "Service_Flag", "Notes"
]

def run_connection_test():
    # Fix for terminal encoding issues
    sys.stdout.reconfigure(encoding='utf-8')
    print("--- 🚗 Tiguan Trakker: Connection & Schema Test ---")

    try:
        # 1. Authenticate
        client = auth.get_gspread_client()
        
        # 2. Open Spreadsheet
        spreadsheet = client.open("Tiguan_Master_Log")
        sheet = spreadsheet.get_worksheet(0) # Selects 'Sheet1'
        
        print(f"Test Status: PASSED ✅")
        print(f"Connected to: {spreadsheet.title}")
        print(f"Active Worksheet: {sheet.title}")

        # 3. Apply Schema (Optional: Run this to force Row 1 to match our headers)
        print("\nVerifying Headers...")
        current_row1 = sheet.row_values(1)
        
        if current_row1 != TIGUAN_HEADERS:
            print("Updating Row 1 to match Master Headers...")
            # We use 'A1' as the start. gspread handles the range.
            sheet.update('A1', [TIGUAN_HEADERS])
            print("Headers Updated! ✅")
        else:
            print("Headers already match Master Schema. ✅")

        # 4. Final Data Integrity Check
        # Let's try to pull Row 2 to see if there is any "ghost" data
        sample_data = sheet.row_values(2)
        if sample_data:
            print(f"Existing Data Found in Row 2: {sample_data}")
        else:
            print("Row 2 is empty. Ready for first import.")

    except gspread.exceptions.SpreadsheetNotFound:
        print("Test Status: FAILED ❌")
        print("Error: 'Tiguan_Master_Log' not found. Ensure it is shared with the service account email.")
    except Exception as e:
        print("Test Status: FAILED ❌")
        print(f"Error: {e}")

if __name__ == "__main__":
    run_connection_test()