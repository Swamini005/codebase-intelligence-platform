from typing import List
from sqlalchemy.orm import Session
from backend.data_access.base import BaseDAO
from backend.models.file import File

class FileDAO(BaseDAO[File]):
    def __init__(self):
        super().__init__(File)

    def get_by_repository(self, db: Session, repository_id: int) -> List[File]:
        return db.query(self.model).filter(self.model.repository_id == repository_id).all()

file_dao = FileDAO()
