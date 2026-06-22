from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.db.session import get_db
from backend.schemas.analysis import ArchitectureResponse, DependencyGraphResponse
from backend.services.architecture import ArchitectureService
from backend.api.dependencies import get_architecture_service

router = APIRouter()

@router.get("/{id}/architecture", response_model=ArchitectureResponse)
def get_architecture(
    id: int,
    db: Session = Depends(get_db),
    arch_service: ArchitectureService = Depends(get_architecture_service)
):
    """GET /repositories/{id}/architecture - Visualizes architectural module layout."""
    data = arch_service.get_architecture_overview(db, repo_id=id)
    return ArchitectureResponse(
        repository_id=id,
        modules=data.get("modules", [])
    )

@router.get("/{id}/dependencies", response_model=DependencyGraphResponse)
def get_dependencies(
    id: int,
    db: Session = Depends(get_db),
    arch_service: ArchitectureService = Depends(get_architecture_service)
):
    """GET /repositories/{id}/dependencies - Returns dependency graph nodes and edges."""
    data = arch_service.get_dependency_graph(db, repo_id=id)
    return DependencyGraphResponse(
        repository_id=id,
        nodes=data.get("nodes", []),
        edges=data.get("edges", [])
    )
