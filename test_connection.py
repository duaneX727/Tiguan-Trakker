import auth
import sys
import gspread
import csv # Make sure this is at the top of your file too!

# Add this at the bottom of your file
csv_filename = 'cleaned_Tiguan_logs.csv'

sys.stdout.reconfigure(encoding='utf-8')
print("--- Tiguan Trakker: Connection Test ---")

try:
    client = auth.get_gspread_client()
    spreadsheet = client.open("Tiguan_Master_Log")
    
    # Step 2: Select the first worksheet (tab)
    sheet = spreadsheet.get_worksheet(0) 
    
    print(f"Test Status: PASSED ✅")
    print(f"Connected to Spreadsheet: {spreadsheet.title}")
    print(f"Connected to Worksheet: {sheet.title}")

    # Testing Data Retrieval: Pull the first row (headers)
    # The exact headers from your CSV file
    target_headers = [
    "Date", "Odometer", "Trip", "Fuel_Type", 
    "Gallons", "Cost", "MPG", "Status"
    ]
    # This clears row 1 and sets the new headers
    sheet.update('A1:H1', [target_headers])
    print("Headers updated to match CSV structure!")
    headers = sheet.row_values(2)
    
    if headers:
        print(f"Successfully retrieved headers: {headers}")
    else:
        print("Connected, but the sheet appears to be empty.")

except gspread.exceptions.SpreadsheetNotFound:
    print("Test Status: FAILED ❌")
    print("Error: Spreadsheet 'Tiguan_Master_Log' not found. Check sharing settings.")
except Exception as e:
    print(f"Test Status: FAILED ❌")
    print(f"Error: {e}")
    
    
try:
    with open(csv_filename, mode='r', encoding='utf-8') as f:
        reader = csv.reader(f)
        headers_in_csv = next(reader)
        
        # This is the logic that filters out those empty rows we saw in your CSV
        rows_to_upload = [row for row in reader if any(field.strip() for field in row)]
        
        print(f"Found {len(rows_to_upload)} rows of actual data in the CSV.")
        if rows_to_upload:
            print(f"First row to be uploaded looks like: {rows_to_upload[0]}")
            
except FileNotFoundError:
    print(f"Error: Could not find '{csv_filename}'. Make sure it's in the Tiguan-Project folder.")


    print(f"\n--- Testing CSV Read: {csv_filename} ---")