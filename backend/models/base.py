from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class BaseModel:
    """Mix-in for standard fields."""
    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now(), default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now(), default=datetime.utcnow)
