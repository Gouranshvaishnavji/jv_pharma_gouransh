import os
import uuid
import mimetypes

UPLOAD_DIR = "data/uploads"

def ensure_directory(path):
    os.makedirs(path, exist_ok=True)

def save_uploaded_file(file_id: str, file):
    folder = os.path.join(UPLOAD_DIR, file_id)
    ensure_directory(folder)

    file_path = os.path.join(folder, file.filename)

    with open(file_path, "wb") as f:
        f.write(file.file.read())

    return file_path

def get_file_type(file_path: str) -> str:
    mime, _ = mimetypes.guess_type(file_path)

    if mime is None:
        return "unknown"

    if "pdf" in mime:
        return "pdf"
    if "word" in mime or file_path.endswith(".docx"):
        return "docx"
    if "text" in mime:
        return "txt"
    if "image" in mime:
        return "image"

    return "unknown"
