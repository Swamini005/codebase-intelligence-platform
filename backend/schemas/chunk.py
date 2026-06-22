from backend.schemas.base import BaseSchema, BaseModel

class CodeChunkBase(BaseModel):
    chunk_text: str
    start_line: int
    end_line: int

class CodeChunkResponse(BaseSchema, CodeChunkBase):
    file_id: int
