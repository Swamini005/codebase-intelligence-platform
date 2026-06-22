from sqlalchemy import ForeignKey, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import Any, Dict
from backend.models.base import Base, BaseModel
from backend.shared.enums import AnalysisType

class AnalysisResult(Base, BaseModel):
    __tablename__ = "analysis_results"

    repository_id: Mapped[int] = mapped_column(ForeignKey("repositories.id", ondelete="CASCADE"), nullable=False)
    analysis_type: Mapped[AnalysisType] = mapped_column(SQLEnum(AnalysisType), nullable=False)
    result_json: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False)

    # Relationships
    repository: Mapped["Repository"] = relationship("Repository", back_populates="analysis_results")
