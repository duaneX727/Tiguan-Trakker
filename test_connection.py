import auth
import sys
import gspread

sys.stdout.reconfigure(encoding='utf-8')
print("--- Tiguan Trakker: Connection Test ---")

try:
    client = auth.get_gspread_client()
    
    # This line connects the script to your actual spreadsheet
    sheet = client.open("Tiguan_Master_Log") 
    
    print(f"Connected to: {sheet.title}")
    print("Test Status: PASSED ✅")

except Exception as e:
    print(f"Test Status: FAILED ❌")
    print(f"Error: {e}")