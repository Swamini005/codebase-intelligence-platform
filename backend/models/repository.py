import datetime
from sqlalchemy import ForeignKey, String, Enum as SQLEnum, DateTime
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
    cloned_at: Mapped[Optional[datetime.datetime]] = mapped_column(DateTime, nullable=True)
    file_count: Mapped[int] = mapped_column(default=0, nullable=False)
    error_message: Mapped[Optional[str]] = mapped_column(String(1024), nullable=True)

    @property
    def owner_id(self) -> int:
        return self.user_id

    @owner_id.setter
    def owner_id(self, value: int):
        self.user_id = value


    # Relationships
    user: Mapped["User"] = relationship("User", back_populates="repositories")
    files: Mapped[List["File"]] = relationship("File", back_populates="repository", cascade="all, delete-orphan")
    chat_sessions: Mapped[List["ChatSession"]] = relationship("ChatSession", back_populates="repository", cascade="all, delete-orphan")
    analysis_results: Mapped[List["AnalysisResult"]] = relationship("AnalysisResult", back_populates="repository", cascade="all, delete-orphan")
    symbols: Mapped[List["Symbol"]] = relationship("Symbol", back_populates="repository", cascade="all, delete-orphan")
