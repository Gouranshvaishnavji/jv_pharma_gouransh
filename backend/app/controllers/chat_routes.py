from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.core.logger import setup_logger

logger = setup_logger()
router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None

@router.post("/ask")
async def ask_chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="query cannot be empty")

    logger.info(f"chat query received: {request.query}")
    return {
        "response": "this is a placeholder answer. Retrieval will be added soon",
        "citations": []
    }