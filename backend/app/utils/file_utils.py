import shutil
import uuid
import mimetypes
from pathlib import Path
from fastapi import UploadFile
from app.core.errors import CustomAPIError
from app.core.config import settings

MAX_FILE_SIZE_MB = 20  # you can move to config later
ALLOWED_MIME_TYPES = [
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "text/plain"
]

def save_uploaded_file(file: UploadFile, upload_base_dir: Path) -> dict:
    """
    it saves an uploaded file to a unique UUID-based subdirectory.
    then performs MIME-type and size validation.
    and returns metadata about the saved file.
    """

    # --- Validate content type ---
    mime_type = file.content_type or mimetypes.guess_type(file.filename)[0]
    if mime_type not in ALLOWED_MIME_TYPES:
        raise CustomAPIError(
            message=f"Unsupported file type: {mime_type}",
            status_code=415,
            error_code="UNSUPPORTED_FILE_TYPE"
        )

    # --- Create subdirectory for this upload ---
    doc_id = str(uuid.uuid4())
    upload_dir = upload_base_dir / doc_id
    upload_dir.mkdir(parents=True, exist_ok=True)

    file_path = upload_dir / file.filename

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    size_mb = file_path.stat().st_size / (1024 * 1024)
    if size_mb > MAX_FILE_SIZE_MB:
        file_path.unlink(missing_ok=True)
        raise CustomAPIError(
            message=f"File exceeds size limit ({MAX_FILE_SIZE_MB} MB)",
            status_code=400,
            error_code="FILE_TOO_LARGE"
        )

    return {
        "file_name": file.filename,
        "file_path": str(file_path),
        "mime_type": mime_type,
        "size_mb": round(size_mb, 2),
        "doc_id": doc_id,
    }
def extract_text_from_file(file_path: Path) -> str:

    from unstructured.partition.auto import partition #a good strategy to reduce loading time

    elements = partition(filename=str(file_path))
    text = "\n".join([el.text for el in elements if hasattr(el, "text")])
    return text
