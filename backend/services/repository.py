from abc import ABC, abstractmethod
from typing import List, Optional
from sqlalchemy.orm import Session
from backend.models.repository import Repository
from backend.shared.enums import RepositoryStatus
from backend.schemas.repository import RepositoryCreateUpload, RepositoryCreateGithub

class RepositoryService(ABC):
    @abstractmethod
    def create_from_upload(self, db: Session, user_id: int, repo_in: RepositoryCreateUpload) -> Repository:
        """Create a repository metadata entry from zipped code upload."""
        pass

    @abstractmethod
    def create_from_github(self, db: Session, user_id: int, repo_in: RepositoryCreateGithub) -> Repository:
        """Create a repository metadata entry by connecting a GitHub URL."""
        pass

    @abstractmethod
    def get_repository(self, db: Session, repo_id: int) -> Optional[Repository]:
        """Fetch repository by ID."""
        pass

    @abstractmethod
    def get_all_repositories(self, db: Session, user_id: int) -> List[Repository]:
        """Fetch all repositories owned by a user."""
        pass

    @abstractmethod
    def trigger_indexing(self, db: Session, repo_id: int) -> bool:
        """Start the code indexing pipeline asynchronously."""
        pass

    @abstractmethod
    def get_status(self, db: Session, repo_id: int) -> RepositoryStatus:
        """Get indexing status of a repository."""
        pass


class RepositoryServiceImpl(RepositoryService):
    def create_from_upload(self, db: Session, user_id: int, repo_in: RepositoryCreateUpload) -> Repository:
        # Stub implementation
        from backend.data_access.repository_dao import repository_dao
        return repository_dao.create(db, obj_in={
            "user_id": user_id,
            "name": repo_in.name,
            "status": RepositoryStatus.PENDING
        })

    def create_from_github(self, db: Session, user_id: int, repo_in: RepositoryCreateGithub) -> Repository:
        # Stub implementation
        from backend.data_access.repository_dao import repository_dao
        name = repo_in.github_url.split("/")[-1].replace(".git", "")
        return repository_dao.create(db, obj_in={
            "user_id": user_id,
            "name": name,
            "github_url": repo_in.github_url,
            "status": RepositoryStatus.PENDING
        })

    def get_repository(self, db: Session, repo_id: int) -> Optional[Repository]:
        from backend.data_access.repository_dao import repository_dao
        return repository_dao.get(db, repo_id)

    def get_all_repositories(self, db: Session, user_id: int) -> List[Repository]:
        from backend.data_access.repository_dao import repository_dao
        return repository_dao.get_by_user(db, user_id)

    def trigger_indexing(self, db: Session, repo_id: int) -> bool:
        # Stub to trigger indexing pipeline
        from backend.data_access.repository_dao import repository_dao
        repository_dao.update_status(db, repo_id, RepositoryStatus.INDEXING)
        # TODO: Call background service/threads to run parsing, embedding, storing
        return True

    def get_status(self, db: Session, repo_id: int) -> RepositoryStatus:
        from backend.data_access.repository_dao import repository_dao
        repo = repository_dao.get(db, repo_id)
        if not repo:
            return RepositoryStatus.FAILED
        return repo.status
