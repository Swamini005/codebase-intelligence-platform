from fastapi import APIRouter, Depends, UploadFile, File as FastAPIFile, HTTPException
from sqlalchemy.orm import Session
from typing import List
import datetime
from backend.db.session import get_db
from backend.schemas.repository import RepositoryResponse, RepositoryCreateUpload, RepositoryCreateGithub, RepositoryIndexStatus
from backend.schemas.symbol import SymbolResponse
from backend.services.repository import RepositoryService
from backend.api.dependencies import get_repository_service
from backend.shared.enums import RepositoryStatus, SymbolType

router = APIRouter()

@router.post("/upload", response_model=RepositoryResponse)
def upload_repository(
    name: str,
    file: UploadFile = FastAPIFile(...),
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/upload - Handle file upload and create repo record."""
    repo_in = RepositoryCreateUpload(name=name)
    # Stub user_id = 1
    return repo_service.create_from_upload(db, user_id=1, repo_in=repo_in)

@router.post("/github", response_model=RepositoryResponse)
def connect_github(
    repo_in: RepositoryCreateGithub,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/github - Connect external GitHub repository."""
    # Stub user_id = 1
    return repo_service.create_from_github(db, user_id=1, repo_in=repo_in)

@router.get("", response_model=List[RepositoryResponse])
def list_repositories(
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """GET /repositories - List all user repositories."""
    return repo_service.get_all_repositories(db, user_id=1)

@router.get("/{id}", response_model=RepositoryResponse)
def get_repository(
    id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """GET /repositories/{id} - Get repo metadata."""
    repo = repo_service.get_repository(db, repo_id=id)
    if not repo:
        raise HTTPException(status_code=404, detail="Repository not found")
    return repo

@router.post("/{id}/index", response_model=RepositoryIndexStatus)
def trigger_index(
    id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/{id}/index - Trigger parsing/embedding/indexing."""
    success = repo_service.trigger_indexing(db, repo_id=id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to start indexing")
    status = repo_service.get_status(db, repo_id=id)
    return RepositoryIndexStatus(repository_id=id, status=status)

@router.get("/{id}/status", response_model=RepositoryIndexStatus)
def get_index_status(
    id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """GET /repositories/{id}/status - Fetch indexing progress status."""
    status = repo_service.get_status(db, repo_id=id)
    return RepositoryIndexStatus(repository_id=id, status=status)

@router.post("/{id}/reindex", response_model=RepositoryIndexStatus)
def trigger_reindex(
    id: int,
    db: Session = Depends(get_db),
    repo_service: RepositoryService = Depends(get_repository_service)
):
    """POST /repositories/{id}/reindex - Trigger full re-indexing of a repository."""
    # Reset status to pending then indexing
    success = repo_service.trigger_indexing(db, repo_id=id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to trigger reindexing")
    status = repo_service.get_status(db, repo_id=id)
    return RepositoryIndexStatus(repository_id=id, status=status)

@router.get("/{id}/symbols", response_model=List[SymbolResponse])
def get_repository_symbols(
    id: int,
    db: Session = Depends(get_db)
):
    """GET /repositories/{id}/symbols - Return extracted functions, classes, interfaces, and enums."""
    # Stub response matching SymbolResponse schema
    now = datetime.datetime.utcnow()
    return [
        SymbolResponse(
            id=1,
            repository_id=id,
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
            repository_id=id,
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
