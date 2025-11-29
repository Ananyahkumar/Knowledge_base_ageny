from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import subprocess
import sys

# Ensure UTF-8 output
sys.stdout.reconfigure(encoding='utf-8')

# OFFLINE embedding model
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

# FULL PATH TO OLLAMA.EXE (confirmed from your system)
OLLAMA_PATH = r"C:\Users\anany\AppData\Local\Programs\Ollama\ollama.exe"

def load_retriever():
    db = Chroma(
        persist_directory="chroma_db",
        embedding_function=embeddings
    )
    return db.as_retriever(search_kwargs={"k": 2})

def run_ollama(prompt):
    # Run ollama with UTF-8 safe encoding
    result = subprocess.run([OLLAMA_PATH, "run", "phi3"],
                        input=prompt.encode("utf-8"),
                        stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE,
                        text=False)
    # Decode output safely
    return result.stdout.decode("utf-8", errors="ignore")

def make_qa_chain():
    retriever = load_retriever()

    def answer(query):
        docs = retriever.invoke(query)
        context = "\n\n".join([d.page_content for d in docs])
        context = context[:1200]

        prompt = f"""
Answer the question using the context below.
If the answer is not in the context, say "I don't know".

Context:
{context}

Question: {query}

Answer:
"""
        return run_ollama(prompt)

    return answer
