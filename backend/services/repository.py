import datetime
import logging
import asyncio
from typing import Optional, List, Any
from sqlalchemy.orm import Session
from backend.core.config import Settings
from backend.models.repository import Repository
from backend.shared.enums import RepositoryStatus
from backend.integrations.github.service import GitHubService
from backend.data_access.repository_dao import repository_dao, RepositoryDAO
from backend.core.exceptions import (
    ProcessingException,
    RepoNotFoundException,
    RepoCloneException,
    GitHubException
)

logger = logging.getLogger(__name__)

class RepositoryService:
    def __init__(self, db: Optional[Any] = None, settings: Optional[Settings] = None):
        from backend.core.config import settings as global_settings
        self.settings = settings or global_settings
        self.db = db
        self.github_service = GitHubService(self.settings)
        logger.info("Initialized RepositoryService")

    async def ingest_repository(self, github_url: str, user_id: int, db: Optional[Any] = None) -> dict:
        """Ingest a repository from GitHub.
        
        1. Checks for existing record.
        2. Creates a processing record.
        3. Clones the repository in a threadpool.
        4. Updates DB record upon success/failure.
        """
        active_db = db or self.db
        if active_db is None:
            raise ValueError("No database session provided")

        from sqlalchemy import select
        from sqlalchemy.ext.asyncio import AsyncSession

        # Step 1: Check if repository record already exists
        if isinstance(active_db, AsyncSession):
            stmt = select(Repository).where(Repository.github_url == github_url)
            result = await active_db.execute(stmt)
            repo = result.scalars().first()
        else:
            repo = active_db.query(Repository).filter(Repository.github_url == github_url).first()

        if repo:
            if repo.status == RepositoryStatus.processing:
                raise ProcessingException("Already in progress")
            elif repo.status == RepositoryStatus.completed:
                return {
                    "id": repo.id,
                    "github_url": repo.github_url,
                    "status": "completed",
                    "local_path": str(self.github_service.get_local_path(github_url)),
                    "cloned_at": repo.cloned_at.isoformat() if repo.cloned_at else None
                }

        # Step 2: Create or update Repository DB record to "processing"
        if not repo:
            owner, repo_name = self.github_service.client.parse_github_url(github_url)
            repo = Repository(
                name=repo_name,
                github_url=github_url,
                status=RepositoryStatus.processing,
                owner_id=user_id,
                cloned_at=None,
                file_count=0
            )
            active_db.add(repo)
        else:
            repo.status = RepositoryStatus.processing
            repo.owner_id = user_id
            repo.cloned_at = None
            repo.file_count = 0
            repo.error_message = None

        if isinstance(active_db, AsyncSession):
            await active_db.commit()
            await active_db.refresh(repo)
        else:
            active_db.commit()
            active_db.refresh(repo)

        # Step 3: Call clone_repo in a threadpool
        loop = asyncio.get_event_loop()
        try:
            local_path = await loop.run_in_executor(
                None,
                self.github_service.clone_repo,
                github_url
            )
            
            repo.cloned_at = datetime.datetime.utcnow()
            repo.status = RepositoryStatus.completed
            
            if isinstance(active_db, AsyncSession):
                await active_db.commit()
                await active_db.refresh(repo)
            else:
                active_db.commit()
                active_db.refresh(repo)
                
        except Exception as e:
            repo.status = RepositoryStatus.failed
            repo.error_message = str(e)
            if isinstance(active_db, AsyncSession):
                await active_db.commit()
            else:
                active_db.commit()
            raise

        # Step 4: Return details
        return {
            "id": repo.id,
            "github_url": github_url,
            "status": "cloned",
            "local_path": str(local_path),
            "cloned_at": repo.cloned_at.isoformat() if repo.cloned_at else None
        }

    async def get_repository(self, *args, **kwargs) -> Optional[Repository]:
        """Fetch repository from DB by ID."""
        active_db = self.db
        repo_id = None
        
        if len(args) == 2:
            active_db = args[0]
            repo_id = args[1]
        elif len(args) == 1:
            repo_id = args[0]
            
        if "repo_id" in kwargs:
            repo_id = kwargs["repo_id"]
        if "db" in kwargs:
            active_db = kwargs["db"]

        if active_db is None:
            raise ValueError("No database session provided")

        from sqlalchemy.ext.asyncio import AsyncSession
        if isinstance(active_db, AsyncSession):
            return await active_db.get(Repository, repo_id)
        else:
            return active_db.query(Repository).filter(Repository.id == repo_id).first()

    async def delete_repository(self, *args, **kwargs) -> None:
        """Delete local cloned repo and DB record."""
        active_db = self.db
        repo_id = None
        
        if len(args) == 2:
            active_db = args[0]
            repo_id = args[1]
        elif len(args) == 1:
            repo_id = args[0]
            
        if "repo_id" in kwargs:
            repo_id = kwargs["repo_id"]
        if "db" in kwargs:
            active_db = kwargs["db"]

        if active_db is None:
            raise ValueError("No database session provided")

        repo = await self.get_repository(repo_id, db=active_db)
        if not repo:
            raise FileNotFoundError(f"Repository with id {repo_id} not found")
            
        if repo.github_url:
            try:
                self.github_service.delete_repo(repo.github_url)
            except FileNotFoundError:
                pass

        from sqlalchemy.ext.asyncio import AsyncSession
        if isinstance(active_db, AsyncSession):
            await active_db.delete(repo)
            await active_db.commit()
        else:
            active_db.delete(repo)
            active_db.commit()

    # Legacy Compatibility methods
    def create_from_upload(self, db: Session, user_id: int, repo_in: Any) -> Repository:
        return repository_dao.create(db, obj_in={
            "user_id": user_id,
            "name": repo_in.name,
            "status": RepositoryStatus.PENDING
        })

    def create_from_github(self, db: Session, user_id: int, repo_in: Any) -> Repository:
        name = repo_in.github_url.split("/")[-1].replace(".git", "")
        return repository_dao.create(db, obj_in={
            "user_id": user_id,
            "name": name,
            "github_url": repo_in.github_url,
            "status": RepositoryStatus.PENDING
        })

    def get_all_repositories(self, db: Session, user_id: int) -> List[Repository]:
        return repository_dao.get_by_user(db, user_id)

    def trigger_indexing(self, db: Session, repo_id: int) -> bool:
        repository_dao.update_status(db, repo_id, RepositoryStatus.INDEXING)
        return True

    def get_status(self, db: Session, repo_id: int) -> RepositoryStatus:
        repo = repository_dao.get(db, repo_id)
        if not repo:
            return RepositoryStatus.FAILED
        return repo.status

class RepositoryServiceImpl(RepositoryService):
    pass

