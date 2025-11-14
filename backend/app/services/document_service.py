from pathlib import Path
import json
from app.utils.file_utils import save_uploaded_file
from app.utils.text_extractors import extract_text_from_file
from app.utils.text_utils import clean_text, chunk_text, save_chunks_to_jsonl
from app.db.vector_db import add_documents
from app.core.logger import setup_logger
from app.core.config import settings

logger = setup_logger()

def process_and_store_docs(files):
    processed_docs = []
    for file in files:
        meta = save_uploaded_file(file, settings.UPLOAD_DIR)
        file_path = Path(meta["file_path"])
        text = extract_text_from_file(file_path)
        text_path = file_path.with_suffix(".txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(text)

        cleaned_text = clean_text(text)
        chunks = chunk_text(cleaned_text, source_path=file_path, doc_id=meta["doc_id"])
        chunks_path = file_path.with_suffix(".jsonl")
        save_chunks_to_jsonl(chunks, chunks_path)

        added = add_documents(chunks)

        meta.update({
            "extracted_text_path": str(text_path),
            "chunks_path": str(chunks_path),
            "chunk_count": len(chunks),
            "char_count": len(cleaned_text),
            "added_to_db": added
        })

        processed_docs.append(meta)
        logger.info(f"{meta['file_name']}: {len(chunks)} chunks added to DB")

    return processed_docs
