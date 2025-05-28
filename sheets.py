import gspread
import json
import os
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials
import base64

load_dotenv()

SPREADSHEET_ID = os.getenv("SPREADSHEET_ID")
SHEET_NAME = "Sheet1"
CACHE_FILE = "cache.json"

# Ambil credential dari ENV dan buat file sementara
def get_credentials_file():
    encoded = os.getenv("GOOGLE_CREDENTIALS_BASE64")
    if not encoded:
        raise Exception("GOOGLE_CREDENTIALS_BASE64 not found in ENV")
    decoded = base64.b64decode(encoded)
    with open("temp_credentials.json", "wb") as f:
        f.write(decoded)
    return "temp_credentials.json"

def fetch_data():
    credentials_path = get_credentials_file()
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID).worksheet(SHEET_NAME)
    data = sheet.get_all_records()

    with open(CACHE_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)

def get_cached_data():
    try:
        with open(CACHE_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []
