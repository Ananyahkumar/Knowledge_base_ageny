# sheets_logger.py
# Robust helper to load GCP credentials from Streamlit secrets (base64) and append logs to a Google Sheet.
# Safe: catches import errors and surfaces helpful messages to Streamlit logs.

import streamlit as st
import json
import base64
import logging

# Try to import Google libs; if missing, show clear error message
try:
    from google.oauth2.service_account import Credentials
    from googleapiclient.discovery import build
except Exception as e:
    # Import error will be visible in Streamlit logs and as an exception when this module is imported
    logging.exception("Required Google libraries are missing or failed to import.")
    # Re-raise so Streamlit shows the exact ImportError in logs (but keep message helpful)
    raise

LOG = logging.getLogger(__name__)

def get_credentials():
    """
    Load base64-encoded GCP key from st.secrets['GCP_KEY_B64'],
    decode -> parse JSON -> create Credentials object.
    """
    if "GCP_KEY_B64" not in st.secrets:
        raise KeyError("GCP_KEY_B64 not found in Streamlit secrets. Add your base64 key as GCP_KEY_B64.")

    base64_key = st.secrets["GCP_KEY_B64"]
    try:
        key_json = base64.b64decode(base64_key).decode("utf-8")
        key_dict = json.loads(key_json)
    except Exception as e:
        LOG.exception("Failed to decode or parse base64 GCP key.")
        raise RuntimeError("Failed to decode/parse GCP_KEY_B64. Check formatting.") from e

    creds = Credentials.from_service_account_info(
        key_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )
    return creds

def _get_sheets_service():
    creds = get_credentials()
    service = build("sheets", "v4", credentials=creds)
    return service

def log_to_sheets(values, spreadsheet_id: str, range_name: str = "Sheet1!A1", value_input_option: str = "RAW"):
    """
    Append a row or rows to a Google Sheet.
    - values: list of lists (e.g. [[col1, col2, ...], [row2col1, ...]])
    - spreadsheet_id: the Google Sheets ID (from sheet URL)
    - range_name: A1 range or sheet name where to append
    """
    if not isinstance(values, list):
        raise ValueError("values must be a list of rows (each row a list). Example: [[a,b,c], [d,e,f]]")

    try:
        service = _get_sheets_service()
        sheet = service.spreadsheets()
        body = {"values": values}
        result = sheet.values().append(
            spreadsheetId=spreadsheet_id,
            range=range_name,
            valueInputOption=value_input_option,
            insertDataOption="INSERT_ROWS",
            body=body
        ).execute()
        return result
    except Exception as e:
        LOG.exception("Failed to log to Google Sheets.")
        # Show message in Streamlit logs (do not leak secrets)
        st.error("Failed to write to Google Sheets — check app logs and credentials.")
        raise
