import auth

print("--- Tiguan Trakker: Connection Test ---")

try:
    # Initialize the client using your service account credentials
    client = auth.get_gspread_client()
    
    # Try to open the specific master log sheet
    sheet = client.open("Tiguan_Master_Log")
    
    print(f"Connected to: {sheet.title}")
    print("Test Status: PASSED ✅")
except Exception as e:
    print(f"Test Status: FAILED ❌")
    print(f"Error: {e}")