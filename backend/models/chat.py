from sqlalchemy import ForeignKey, Text, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from backend.models.base import Base, BaseModel
from backend.shared.enums import ChatMessageRole

class ChatSession(Base, BaseModel):
    __tablename__ = "chat_sessions"

    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)

    # Relationships
    repository: Mapped["Repository"] = relationship("Repository", back_populates="chat_sessions")
    messages: Mapped[List["ChatMessage"]] = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")

class ChatMessage(Base, BaseModel):
    __tablename__ = "chat_messages"

    session_id: Mapped[int] = mapped_column(ForeignKey("chat_sessions.id", ondelete="CASCADE"), nullable=False)
    role: Mapped[ChatMessageRole] = mapped_column(SQLEnum(ChatMessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # Relationships
    session: Mapped["ChatSession"] = relationship("ChatSession", back_populates="messages")
