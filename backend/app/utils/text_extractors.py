from pathlib import Path
import pdfplumber
from docx import Document
from PIL import Image
import pytesseract
from app.core.errors import CustomAPIError
from app.core.logger import setup_logger

logger = setup_logger()

def extract_text_from_file(file_path: Path) -> str:
    """
    Extract plain text from a file (PDF, DOCX, TXT, or image).
    Returns the extracted text as a string.
    """
    if not file_path.exists():
        raise CustomAPIError(
            message=f"File not found: {file_path}",
            status_code=404,
            error_code="FILE_NOT_FOUND"
        )

    suffix = file_path.suffix.lower()

    try:
        if suffix == ".pdf":
            text = extract_text_pdf(file_path)
        elif suffix in [".docx", ".doc"]:
            text = extract_text_docx(file_path)
        elif suffix == ".txt":
            text = extract_text_txt(file_path)
        elif suffix in [".png", ".jpg", ".jpeg"]:
            text = extract_text_image(file_path)
        else:
            logger.warning(f"Unsupported file extension {suffix}, treating as plain text")
            text = extract_text_txt(file_path)

        return text.strip()

    except Exception as e:
        logger.error(f"Error extracting text from {file_path}: {e}")
        raise CustomAPIError(
            message=f"Failed to extract text from {file_path.name}",
            status_code=500,
            error_code="TEXT_EXTRACTION_FAILED"
        )


def extract_text_pdf(file_path: Path) -> str:
    text = ""
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() or ""
    return text


def extract_text_docx(file_path: Path) -> str:
    doc = Document(file_path)
    return "\n".join([p.text for p in doc.paragraphs])


def extract_text_txt(file_path: Path) -> str:
    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def extract_text_image(file_path: Path) -> str:
    try:
        image = Image.open(file_path)
        text = pytesseract.image_to_string(image)
        return text
    except Exception as e:
        logger.warning(f"OCR failed for {file_path}: {e}")
        return ""