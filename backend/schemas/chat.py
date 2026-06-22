from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from backend.shared.enums import ChatMessageRole

class ChatMessageBase(BaseModel):
    role: ChatMessageRole
    content: str

class ChatMessageCreate(ChatMessageBase):
    pass

class ChatMessageResponse(ChatMessageBase):
    id: int
    session_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ChatSessionCreate(BaseModel):
    repository_id: int

class ChatSessionResponse(BaseModel):
    id: int
    repository_id: int
    created_at: datetime
    updated_at: datetime
    messages: List[ChatMessageResponse] = []

    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    repository_id: int
    session_id: Optional[int] = None
    message: str

class ChatResponse(BaseModel):
    session_id: int
    response: str
    # Source code chunks used in generating answer (RAG sources)
    sources: List[str] = []
