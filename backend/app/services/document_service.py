import uuid
from app.utils.file_utils import save_uploaded_file, get_file_type
from app.utils.text_utils import extract_text_from_file, chunk_text
from app.db.vector_db import add_documents

def process_and_store_docs(files):
    results = []

    for file in files:
        file_id = str(uuid.uuid4())
        saved_path = save_uploaded_file(file_id, file)
        file_type = get_file_type(saved_path)

        text = extract_text_from_file(saved_path, file_type)
        chunks = chunk_text(text, saved_path)

        add_documents(chunks)

        results.append({
            "file_id": file_id,
            "file_path": saved_path,
            "chunks": len(chunks)
        })

    return results
