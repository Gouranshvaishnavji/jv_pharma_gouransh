from fastapi import APIRouter
from pydantic import BaseModel
from app.services.qa_service import get_answer
import uuid

router = APIRouter()

class ChatRequest(BaseModel):
    query: str
    session_id: str | None = None

@router.post("/ask")
def ask(request: ChatRequest):
    return get_answer(request.query, request.session_id)
@router.post("/new_session")
def new_session():
    return {"session_id": "session-" + uuid.uuid4().hex}
