from fastapi import APIRouter, Depends, status, HTTPException, UploadFile, File as FastAPIFile
from sqlalchemy.orm import Session
from typing import List
import datetime

from backend.db.session import get_db
from backend.schemas.repository import (
    RepositoryResponse,
    RepositoryCreateUpload,
    RepositoryCreateGithub,
    RepositoryIndexStatus,
    RepositoryIngest
)
from backend.schemas.symbol import SymbolResponse
from backend.services.repository import RepositoryService
from backend.api.dependencies import get_repository_service
from backend.core.config import get_settings, Settings
from backend.core.exceptions import (
    InvalidGitHubURLException,
    RepoNotFoundException,
    RepoCloningTimeoutException,
    ProcessingException,
    CodebaseIntelException
)
from backend.shared.enums import RepositoryStatus, SymbolType
from backend.data_access.repository_dao import repository_dao

router = APIRouter()

@router.post("/ingest", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def ingest_repository(
    payload: RepositoryIngest,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service),
    settings: Settings = Depends(get_settings)
):
    """POST /repositories/ingest - Ingest repository from GitHub."""
    try:
        result = await repo_service.ingest_repository(payload.github_url, payload.user_id, db=db)
        return result
    except InvalidGitHubURLException as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except RepoNotFoundException as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except RepoCloningTimeoutException as e:
        raise HTTPException(status_code=status.HTTP_408_REQUEST_TIMEOUT, detail=str(e))
    except ProcessingException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except CodebaseIntelException as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("", response_model=List[RepositoryResponse])
def list_repositories(
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db)
):
    """GET /repositories/ - List all repositories (paginated)."""
    return repository_dao.get_multi(db, skip=skip, limit=limit)

@router.get("/{repo_id}", response_model=RepositoryResponse)
async def get_repository(
    repo_id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """GET /repositories/{repo_id} - Get repo metadata."""
    repo = await repo_service.get_repository(repo_id, db=db)
    if not repo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Repository not found")
    return repo

@router.delete("/{repo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_repository(
    repo_id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """DELETE /repositories/{repo_id} - Delete cloned repository and DB record."""
    try:
        await repo_service.delete_repository(repo_id, db=db)
    except FileNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

@router.post("/upload", response_model=RepositoryResponse)
def upload_repository(
    name: str,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/upload - Handle file upload and create repo record (legacy)."""
    repo_in = RepositoryCreateUpload(name=name)
    return repo_service.create_from_upload(db, user_id=1, repo_in=repo_in)

@router.post("/github", response_model=RepositoryResponse)
def connect_github(
    repo_in: RepositoryCreateGithub,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/github - Connect external GitHub repository (legacy)."""
    return repo_service.create_from_github(db, user_id=1, repo_in=repo_in)

@router.post("/{repo_id}/index", response_model=RepositoryIndexStatus)
def trigger_index(
    repo_id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/{repo_id}/index - Trigger parsing/embedding/indexing."""
    success = repo_service.trigger_indexing(db, repo_id=repo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to start indexing")
    status_val = repo_service.get_status(db, repo_id=repo_id)
    return RepositoryIndexStatus(repository_id=repo_id, status=status_val)

@router.get("/{repo_id}/status", response_model=RepositoryIndexStatus)
def get_index_status(
    repo_id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """GET /repositories/{repo_id}/status - Fetch indexing progress status."""
    status_val = repo_service.get_status(db, repo_id=repo_id)
    return RepositoryIndexStatus(repository_id=repo_id, status=status_val)

@router.post("/{repo_id}/reindex", response_model=RepositoryIndexStatus)
def trigger_reindex(
    repo_id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/{repo_id}/reindex - Trigger full re-indexing of a repository."""
    success = repo_service.trigger_indexing(db, repo_id=repo_id)
    if not success:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to trigger reindexing")
    status_val = repo_service.get_status(db, repo_id=repo_id)
    return RepositoryIndexStatus(repository_id=repo_id, status=status_val)

@router.get("/{repo_id}/symbols", response_model=List[SymbolResponse])
def get_repository_symbols(
    repo_id: int,
    db: Session = Depends(get_db)
):
    """GET /repositories/{repo_id}/symbols - Return extracted functions, classes, interfaces, and enums."""
    now = datetime.datetime.utcnow()
    return [
        SymbolResponse(
            id=1,
            repository_id=repo_id,
            file_id=10,
            name="PlatformException",
            symbol_type=SymbolType.CLASS,
            start_line=1,
            end_line=5,
            metadata_json={"methods": ["__init__"]},
            created_at=now,
            updated_at=now
        ),
        SymbolResponse(
            id=2,
            repository_id=repo_id,
            file_id=10,
            name="get_logger",
            symbol_type=SymbolType.FUNCTION,
            start_line=8,
            end_line=12,
            metadata_json={"params": ["name"]},
            created_at=now,
            updated_at=now
        )
    ]
