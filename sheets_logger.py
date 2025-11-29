import streamlit as st
import json
import base64
from google.oauth2.service_account import Credentials

def get_credentials():
    # 1. Load Base64 from Streamlit Secrets
    base64_key = st.secrets["GCP_KEY_B64"]

    # 2. Decode Base64 → JSON string
    key_json = base64.b64decode(base64_key).decode("utf-8")

    # 3. JSON → Python dict
    key_dict = json.loads(key_json)

    # 4. Build Credentials object
    creds = Credentials.from_service_account_info(
        key_dict,
        scopes=["https://www.googleapis.com/auth/spreadsheets"]
    )

    return creds
