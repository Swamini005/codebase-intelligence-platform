from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from backend.models.base import Base, BaseModel

class User(Base, BaseModel):
    __tablename__ = "users"

    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    
    # Relationships
    repositories: Mapped[List["Repository"]] = relationship("Repository", back_populates="user", cascade="all, delete-orphan")
