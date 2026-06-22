from typing import List
from sqlalchemy.orm import Session
from backend.data_access.base import BaseDAO
from backend.models.repository import Repository
from backend.shared.enums import RepositoryStatus

class RepositoryDAO(BaseDAO[Repository]):
    def __init__(self):
        super().__init__(Repository)

    def get_by_user(self, db: Session, user_id: int) -> List[Repository]:
        return db.query(self.model).filter(self.model.user_id == user_id).all()

    def update_status(self, db: Session, repo_id: int, status: RepositoryStatus) -> Repository:
        repo = self.get(db, repo_id)
        if not repo:
            raise ValueError(f"Repository with id {repo_id} not found")
        repo.status = status
        db.add(repo)
        db.commit()
        db.refresh(repo)
        return repo

repository_dao = RepositoryDAO()
