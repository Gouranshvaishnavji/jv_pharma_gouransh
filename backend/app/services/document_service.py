# app/services/document_service.py
import os
from pathlib import Path
from fastapi import UploadFile
from app.utils.file_utils import save_uploaded_file
from app.utils.text_extractors import extract_text_from_file

from app.utils.text_utils import chunk_text
from app.core.errors import CustomAPIError
from app.core.logger import setup_logger

from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from app.core.config import settings

logger = setup_logger()
UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
# this func handling file upload, text extraction, chunking, embedding generation, and vector store persistence
async def process_and_store_docs(files: list[UploadFile]):

    processed_docs = []

    try:
        for file in files:
            saved_path = save_uploaded_file(file, UPLOAD_DIR)
            logger.info(f"Saved file: {saved_path}")

            text = extract_text_from_file(saved_path)
            text_file_path = Path(meta["file_path"]).with_suffix(".txt")
            with open(text_file_path, "w", encoding="utf-8") as f:
                f.write(text)
            if not text or len(text.strip()) == 0:
                raise CustomAPIError(
                    message=f"No readable content found in {file.filename}",
                    status_code=422,
                    error_code="EMPTY_DOCUMENT"
                )

            chunks = chunk_text(text)
            logger.info(f"Chunked {len(chunks)} sections from {file.filename}")

            embeddings = GoogleGenerativeAIEmbeddings(
                model="models/embedding-001",
                google_api_key=settings.GEMINI_API_KEY
            )

            vectorstore = Chroma.from_texts(
                texts=chunks,
                embedding=embeddings,
                persist_directory=settings.VECTOR_DB_PATH,
                metadatas=[{"source": file.filename}] * len(chunks)
            )

            vectorstore.persist()
            processed_docs.append({"file": file.filename, "chunks": len(chunks)})

        logger.info(f"processed {len(processed_docs)} document(s) successfully.")
        return processed_docs

    except CustomAPIError as ce:
        raise ce
    except Exception as e:
        logger.exception(f"Document's processing failed: {e}")
        raise CustomAPIError(
            message="error during document processing.",
            status_code=500,
            error_code="PROCESSING_FAILED"
        )
