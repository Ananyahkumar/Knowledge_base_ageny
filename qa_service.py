from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings

import sys
import streamlit as st
from groq import Groq

# Create Groq client using secret key from Streamlit (NOT os.environ)
client = None
try:
    if hasattr(st, 'secrets') and "GROQ_API_KEY" in st.secrets:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except (KeyError, AttributeError, RuntimeError) as e:
    # Handle case where secrets might not be available
    import warnings
    warnings.warn("GROQ_API_KEY not found in Streamlit secrets. Make sure to configure it in .streamlit/secrets.toml")

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# Embedding model
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def load_retriever():
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db.as_retriever(search_kwargs={"k": 2})

def run_llm(prompt: str) -> str:
    """Safely call Groq LLM."""
    if not prompt or prompt.strip() == "":
        return "Please enter a valid question."
    
    if client is None:
        return "Error: Groq API key not configured. Please add GROQ_API_KEY to .streamlit/secrets.toml"

    # Hard safety: reduce prompt size (Groq limits context)
    prompt = prompt[:4000]  # ensure size is manageable

    try:
        # Use a currently supported Groq model
        # Default to llama-3.1-8b-instant (replacement for deprecated llama3-8b-8192)
        # Can be overridden via secrets: st.secrets.get("GROQ_MODEL", "llama-3.1-8b-instant")
        model_name = "llama-3.1-8b-instant"
        try:
            if hasattr(st, 'secrets') and "GROQ_MODEL" in st.secrets:
                model_name = st.secrets["GROQ_MODEL"]
        except Exception:
            pass  # Use default if secrets not available
        
        response = client.chat.completions.create(
            model=model_name,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Answer accurately using the context."},
                {"role": "user", "content": prompt}
            ]
        )
        return response.choices[0].message.content

    except Exception as e:
        return f"Groq LLM Error: {str(e)}"

def make_qa_chain():
    retriever = load_retriever()

    def answer(query):
        if not query.strip():
            return "Please enter a question."

        # Retrieve top documents
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])

        # Safety: shorten context to avoid BadRequestError
        context = context[:2000]

        prompt = f"""
Answer the question using ONLY the context below.
If the answer is not found, say "I don't know".

Context:
{context}

Question:
{query}

Answer:
"""
        return run_llm(prompt)

    return answer
