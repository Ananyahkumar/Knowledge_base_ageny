from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import SentenceTransformerEmbeddings
import os

# OFFLINE embedding model wrapper
embeddings = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")

def create_chroma(chunks, persist_directory="chroma_db"):
    os.makedirs(persist_directory, exist_ok=True)

    texts = [c["text"] for c in chunks]

    vectordb = Chroma.from_texts(
        texts=texts,
        embedding=embeddings,   # <-- Correct, not model.encode
        persist_directory=persist_directory
    )
    vectordb.persist()
    return vectordb

def load_chroma(persist_directory="chroma_db"):
    return Chroma(
        persist_directory=persist_directory,
        embedding_function=embeddings
    )
