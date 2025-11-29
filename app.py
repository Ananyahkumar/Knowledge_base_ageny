import streamlit as st
from ingest import pdf_to_text, chunk_text
from vector_store import create_chroma
from qa_service import make_qa_chain
from sheets_logger import log_to_sheets
from datetime import datetime

st.set_page_config(page_title="Knowledge Base Agent", layout="wide")

st.title("📘 Knowledge Base Agent (RAG + LLaMA)")

uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())

    text = pdf_to_text("temp.pdf")
    chunks = chunk_text(text)

    with st.spinner("Indexing locally..."):
        create_chroma(chunks)

    st.success("Document processed offline!")

query = st.text_input("Ask a question about the document:")

# Get spreadsheet ID from secrets, or use placeholder
try:
    SPREADSHEET_ID = st.secrets.get("SPREADSHEET_ID", "YOUR_SHEET_ID_HERE")
except Exception:
    SPREADSHEET_ID = "YOUR_SHEET_ID_HERE"

if st.button("Ask") and query:
    qa = make_qa_chain()

    with st.spinner("Thinking... locally!"):
        answer = qa(query)

        # LOG HERE — after answer exists (non-blocking)
        if SPREADSHEET_ID and SPREADSHEET_ID != "YOUR_SHEET_ID_HERE":
            try:
                log_to_sheets(
                    [[datetime.now().isoformat(), query, answer]],
                    SPREADSHEET_ID,
                    range_name="Sheet1!A:C"  # Use A:C for 3 columns (timestamp, question, answer)
                )
            except Exception as e:
                # Log error but don't crash the app
                st.warning(f"Could not log to Google Sheets: {str(e)}")

    st.subheader("Answer")
    st.write(answer)
