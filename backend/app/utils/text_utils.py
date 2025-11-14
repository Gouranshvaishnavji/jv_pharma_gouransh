import re
import pdfplumber
from docx import Document

def extract_text_from_file(file_path: str, file_type: str) -> str:
    if file_type == "pdf":
        return extract_text_pdf(file_path)
    elif file_type == "docx":
        return extract_text_docx(file_path)
    elif file_type == "txt":
        return extract_text_txt(file_path)
    else:
        return ""

def extract_text_pdf(file_path: str) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return clean_text(text)

def extract_text_docx(file_path: str) -> str:
    doc = Document(file_path)
    text = "\n".join([p.text for p in doc.paragraphs])
    return clean_text(text)

def extract_text_txt(file_path: str) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return clean_text(f.read())

def clean_text(text: str) -> str:
    text = text.replace("\x00", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def chunk_text(text: str, source_path: str, chunk_size=1000, overlap=100):
    chunks = []
    start = 0
    chunk_id = 0

    while start < len(text):
        end = start + chunk_size
        chunk = text[start:end]

        chunks.append({
            "chunk_id": chunk_id,
            "source_path": source_path,
            "text": chunk,
            "start": start,
            "end": end
        })

        chunk_id += 1
        start = end - overlap

    return chunks
