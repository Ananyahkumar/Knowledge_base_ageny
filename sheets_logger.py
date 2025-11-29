from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
import streamlit as st
import json
from google.oauth2.service_account import Credentials

import streamlit as st
st.write("RAW SECRET:", st.secrets["GCP_KEY"])


# ---- CONFIG ----
SHEET_ID = "1NMVAH4ERSChGQfnB9HwacOkQGzB7cEE2AxqZVKQhHs0"
SHEET_NAME = "Sheet1"   # default sheet name


gcp_info = json.loads(st.secrets["GCP_KEY"])

creds = Credentials.from_service_account_info(
    gcp_info,
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
