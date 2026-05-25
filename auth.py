import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

def get_sheet(sheet_name):
    """
    Authenticates with Google Sheets API and returns the specified spreadsheet object.
    """
    # Scope defines what the bot can do (read/write to spreadsheets)
    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]
    
    # Path to your key file, loaded from the .env variable
    creds_path = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
    
    if not creds_path:
        raise ValueError("GOOGLE_APPLICATION_CREDENTIALS environment variable not set.")
        
    try:
        # Authenticate
        creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
        client = gspread.authorize(creds)
        
        # Open the spreadsheet by name
        sheet = client.open(sheet_name).sheet1
        return sheet
        
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

if __name__ == "__main__":
    # Test block to verify connection
    test_sheet = get_sheet("Tiguan Logs")
    if test_sheet:
        print("Successfully connected to Tiguan Logs!")
    else:
        print("Failed to connect.")