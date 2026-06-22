from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.chat import ChatSession, ChatMessage
from backend.shared.enums import ChatMessageRole

class ChatDAO:
    def get_session(self, db: Session, session_id: int) -> Optional[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.id == session_id).first()

    def get_sessions_by_repository(self, db: Session, repository_id: int) -> List[ChatSession]:
        return db.query(ChatSession).filter(ChatSession.repository_id == repository_id).all()

    def create_session(self, db: Session, repository_id: int) -> ChatSession:
        session = ChatSession(repository_id=repository_id)
        db.add(session)
        db.commit()
        db.refresh(session)
        return session

    def delete_session(self, db: Session, session_id: int) -> Optional[ChatSession]:
        session = self.get_session(db, session_id)
        if session:
            db.delete(session)
            db.commit()
        return session

    def add_message(self, db: Session, session_id: int, role: ChatMessageRole, content: str) -> ChatMessage:
        message = ChatMessage(session_id=session_id, role=role, content=content)
        db.add(message)
        db.commit()
        db.refresh(message)
        return message

    def get_messages(self, db: Session, session_id: int) -> List[ChatMessage]:
        return db.query(ChatMessage).filter(ChatMessage.session_id == session_id).order_by(ChatMessage.created_at.asc()).all()

chat_dao = ChatDAO()
