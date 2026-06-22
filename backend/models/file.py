from sqlalchemy import ForeignKey, String, Integer, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from backend.models.base import Base, BaseModel
from backend.shared.enums import FileLanguage

class File(Base, BaseModel):
    __tablename__ = "files"

    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    path: Mapped[str] = mapped_column(String(1024), nullable=False)
    language: Mapped[FileLanguage] = mapped_column(
        SQLEnum(FileLanguage), 
        default=FileLanguage.UNKNOWN, 
        nullable=False
    )
    size: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    # Relationships
    repository: Mapped["Repository"] = relationship("Repository", back_populates="files")
    chunks: Mapped[List["CodeChunk"]] = relationship("CodeChunk", back_populates="file", cascade="all, delete-orphan")
    symbols: Mapped[List["Symbol"]] = relationship("Symbol", back_populates="file", cascade="all, delete-orphan")
