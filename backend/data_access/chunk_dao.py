from typing import List
from sqlalchemy.orm import Session
from backend.data_access.base import BaseDAO
from backend.models.chunk import CodeChunk

class CodeChunkDAO(BaseDAO[CodeChunk]):
    def __init__(self):
        super().__init__(CodeChunk)

    def get_by_file(self, db: Session, file_id: int) -> List[CodeChunk]:
        return db.query(self.model).filter(self.model.file_id == file_id).all()

chunk_dao = CodeChunkDAO()
