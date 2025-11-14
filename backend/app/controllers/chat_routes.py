from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qa_service import get_answer

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None

@router.post("/ask")
async def ask_chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    return get_answer(request.query)
