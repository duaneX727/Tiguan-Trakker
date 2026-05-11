import gspread
from google.oauth2.service_account import Credentials

def get_gspread_client():
    scopes = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    # Ensure service_key.json is in your project folder
    creds = Credentials.from_service_account_file(
        r"C:\Users\Marlon Mitchell\lab-server\K10-Lab\Tiguan-Project\service_key.json",
        scopes=scopes
    )
    client = gspread.authorize(creds) # Now this is part of the function
    return client                     # Now this is part of the function