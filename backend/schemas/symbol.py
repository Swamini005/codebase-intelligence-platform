from typing import Any, Dict, Optional
from backend.schemas.base import BaseSchema, BaseModel
from backend.shared.enums import SymbolType

class SymbolBase(BaseModel):
    name: str
    symbol_type: SymbolType
    start_line: int
    end_line: int
    metadata_json: Optional[Dict[str, Any]] = None

class SymbolResponse(BaseSchema, SymbolBase):
    repository_id: int
    file_id: int
