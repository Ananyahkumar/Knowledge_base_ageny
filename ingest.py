import pdfplumber

def pdf_to_text(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text() or ""
            text += extracted + "\n"
    return text

def chunk_text(text, chunk_size=200, overlap=50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append({"text": chunk})
        i += chunk_size - overlap
    return chunks

