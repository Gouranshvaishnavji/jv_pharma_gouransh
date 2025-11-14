from fastapi import APIRouter, UploadFile, File
from app.services.document_service import process_and_store_docs

router = APIRouter()

@router.post("/upload")
async def upload_documents(files: list[UploadFile] = File(...)):
    return process_and_store_docs(files)
