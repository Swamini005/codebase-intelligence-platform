from sqlalchemy import ForeignKey, String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from backend.models.base import Base, BaseModel
from backend.shared.enums import RepositoryStatus

class Repository(Base, BaseModel):
    __tablename__ = "repositories"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    github_url: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)
    status: Mapped[RepositoryStatus] = mapped_column(
        SQLEnum(RepositoryStatus), 
        default=RepositoryStatus.PENDING, 
        nullable=False
    )

    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="repositories")
    files: Mapped[List["File"]] = relationship("File", back_populates="repository", cascade="all, delete-orphan")
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="repository", cascade="all, delete-orphan")
    analysis_results: Mapped[List["AnalysisResult"]] = relationship("AnalysisResult", back_populates="repository", cascade="all, delete-orphan")
    symbols: Mapped[List["Symbol"]] = relationship("Symbol", back_populates="repository", cascade="all, delete-orphan")
