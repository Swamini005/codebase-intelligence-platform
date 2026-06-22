from backend.schemas.base import BaseSchema, BaseModel
from backend.shared.enums import FileLanguage

class FileBase(BaseModel):
    path: str
    language: FileLanguage
    size: int

class FileResponse(BaseSchema, FileBase):
    repository_id: int
