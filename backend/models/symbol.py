from sqlalchemy import ForeignKey, String, Integer, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, Dict, Optional
from backend.models.base import Base, BaseModel
from backend.shared.enums import SymbolType

class Symbol(Base, BaseModel):
    __tablename__ = "symbols"

    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    file_id: Mapped[int] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    name: Mapped[str] = mapped_column(String(255), index=True, nullable=False)
    symbol_type: Mapped[SymbolType] = mapped_column(
        SQLEnum(SymbolType), 
        nullable=False
    )
    start_line: Mapped[int] = mapped_column(Integer, nullable=False)
    end_line: Mapped[int] = mapped_column(Integer, nullable=False)
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Relationships
    repository: Mapped["Repository"] = relationship("Repository", back_populates="symbols")
    file: Mapped["File"] = relationship("File", back_populates="symbols")
