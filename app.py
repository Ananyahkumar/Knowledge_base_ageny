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

# ---------------------------------------------
# 1. PDF Upload
# ---------------------------------------------
uploaded = st.file_uploader("Upload a PDF file", type=["pdf"])

if uploaded:
    with open("temp.pdf", "wb") as f:
        f.write(uploaded.read())

    text = pdf_to_text("temp.pdf")
    chunks = chunk_text(text)

    with st.spinner("Indexing locally..."):
        create_chroma(chunks)

    st.success("Document processed offline!")

# ---------------------------------------------
# 2. QUESTION INPUT
# ---------------------------------------------
query = st.text_input("Ask a question about the document:")

# Initialize session state for answer
if "answer" not in st.session_state:
    st.session_state.answer = None

# ---------------------------------------------
# 3. ASK BUTTON
# ---------------------------------------------
if st.button("Ask"):
    if not query.strip():
        st.error("Please enter a question.")
    else:
        qa = make_qa_chain()

        with st.spinner("Thinking..."):
            answer = qa(query)
            st.session_state.answer = answer  # store answer safely

            # Only log AFTER successful answer
            log_to_sheets([[datetime.now().isoformat(), query, answer]])

# ---------------------------------------------
# 4. DISPLAY ANSWER
# ---------------------------------------------
if st.session_state.answer:
    st.subheader("Answer")
    st.write(st.session_state.answer)
