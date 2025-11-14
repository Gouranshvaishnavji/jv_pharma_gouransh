
from fastapi import APIRouter, UploadFile, File, status
from app.services.document_service import process_and_store_docs
from app.core.errors import CustomAPIError

router = APIRouter()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_documents(files: list[UploadFile] = File(...)):
    if not files:
        raise CustomAPIError(
            message="No files provided.",
            status_code=400,
            error_code="NO_FILE_UPLOADED"
        )

    results = process_and_store_docs(files)
    return {"success": True, "processed": results}