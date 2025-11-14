from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from app.services.qa_service import get_answer
from app.core.session_manager import create_session, end_session

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None

@router.post("/ask")
async def ask_chat(request: ChatRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    res = get_answer(request.query, request.session_id)
    return res

@router.post("/new_session")
async def new_session():
    return {"session_id": create_session()}

@router.post("/end_session/{session_id}")
async def close_session(session_id: str):
    end_session(session_id)
    return {"success": True}
