from pydantic import HttpUrl, BaseModel
from typing import Optional
from backend.schemas.base import BaseSchema
from backend.shared.enums import RepositoryStatus

class RepositoryBase(BaseModel):
    name: str
    github_url: Optional[str] = None

class RepositoryCreateUpload(BaseModel):
    name: str

class RepositoryCreateGithub(BaseModel):
    github_url: str

class RepositoryResponse(BaseSchema, RepositoryBase):
    user_id: int
    status: RepositoryStatus

class RepositoryIndexStatus(BaseModel):
    repository_id: int
    status: RepositoryStatus

class RepositoryIngest(BaseModel):
    github_url: str
    user_id: int

