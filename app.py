import streamlit as st
from ingest import pdf_to_text, chunk_text
from vector_store import create_chroma
from qa_service import make_qa_chain
from sheets_logger import log_to_sheets
from datetime import datetime

import sys
sys.stdout.reconfigure(encoding='utf-8')

st.set_page_config(page_title="Knowledge Base Agent", layout="wide")

st.title("📘 Knowledge Base Agent (RAG + LLaMA)")

# --------------------------
# Upload PDF
# --------------------------
uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())

    text = pdf_to_text("temp.pdf")
    chunks = chunk_text(text)

    with st.spinner("Indexing locally..."):
        create_chroma(chunks)

    st.success("Document processed offline!")

# --------------------------
# Ask RAG Question
# --------------------------
query = st.text_input("Ask a question about the document:")

if st.button("Ask") and query:
    qa = make_qa_chain()

    with st.spinner("Thinking..."):
        answer = qa(query)

        # CORRECT: Log as a list of rows
        log_to_sheets([[datetime.now().isoformat(), query, answer]])

    st.subheader("Answer")
    st.write(answer)
