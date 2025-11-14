# app/controllers/document_routes.py
from fastapi import APIRouter, UploadFile, File, status
from app.utils.file_utils import save_uploaded_file
from app.core.errors import CustomAPIError
from app.core.logger import setup_logger
from app.core.config import settings

router = APIRouter()
logger = setup_logger()

@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_documents(files: list[UploadFile] = File(...)):
    if not files:
        raise CustomAPIError(
            message="No files provided.",
            status_code=400,
            error_code="NO_FILE_UPLOADED"
        )

    results = []
    for file in files:
        meta = save_uploaded_file(file, settings.UPLOAD_DIR)
        logger.info(f"Uploaded {meta['file_name']} ({meta['size_mb']} MB)")
        results.append(meta)

    return {"success": True, "uploaded": results}
