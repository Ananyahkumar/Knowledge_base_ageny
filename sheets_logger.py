from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# ---- CONFIG ----
SHEET_ID = "1NMVAH4ERSChGQfnB9HwacOkQGzB7cEE2AxqZVKQhHs0"
SHEET_NAME = "Sheet1"   # default sheet name
SERVICE_ACCOUNT_FILE = "gcp_key.json"

# ---- AUTH ----
creds = Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE,
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

service = build("sheets", "v4", credentials=creds)
sheet = service.spreadsheets()

def log_to_sheets(question, answer):
    values = [[question, answer]]
    body = {"values": values}

    sheet.values().append(
        spreadsheetId=SHEET_ID,
        range=f"{SHEET_NAME}!A:B",
        valueInputOption="RAW",
        body=body
    ).execute()
