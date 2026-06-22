from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.services.chat import ChatService
from backend.api.dependencies import get_chat_service

router = APIRouter()

@router.post("", response_model=ChatResponse)
def codebase_chat(
    chat_req: ChatRequest,
    db: Session = Depends(get_db),
    chat_service: ChatService = Depends(get_chat_service)
):
    """POST /chat - Submit chat query to the repository using RAG pipeline."""
    return chat_service.process_chat_message(db, chat_req)
