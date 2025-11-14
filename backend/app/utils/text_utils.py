from pathlib import Path
import json
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
from app.core.logger import setup_logger

logger = setup_logger()


def clean_text(text: str) -> str:
    """
    Normalize whitespace, remove control chars and extra newlines.
    Keeps original order.
    """
    if not text:
        return ""
    text = re.sub(r"[ \t]+", " ", text)        # collapse spaces/tabs
    text = re.sub(r"\r\n|\r", "\n", text)      # normalize newlines
    text = re.sub(r"\n{3,}", "\n\n", text)     # limit consecutive newlines
    text = re.sub(r"[\x00-\x1F\x7F]", "", text)  # remove control chars
    return text.strip()


def chunk_text(
    text: str,
    source_path: Path,
    doc_id: str,
    chunk_size: int = 1000,
    overlap: int = 100,
) -> list[dict]:
    """
    Split text into overlapping chunks with metadata.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=overlap,
        separators=["\n\n", "\n", ".", " ", ""],
    )
    chunks = text_splitter.split_text(text)

    chunk_metadata = []
    cursor = 0
    for i, chunk in enumerate(chunks):
        start = text.find(chunk, cursor)
        end = start + len(chunk)
        cursor = end
        chunk_metadata.append({
            "doc_id": doc_id,
            "chunk_id": f"{doc_id}_{i}",
            "start_char": start,
            "end_char": end,
            "source_path": str(source_path),
            "text": chunk,
        })
    return chunk_metadata


def save_chunks_to_jsonl(chunks: list[dict], output_path: Path):
    """
    Save chunks list to a JSONL file.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    logger.info(f"Saved {len(chunks)} chunks → {output_path}")