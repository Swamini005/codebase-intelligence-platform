from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.db.session import get_db
from backend.services.vectorstore import VectorStoreService
from backend.api.dependencies import get_vectorstore_service

router = APIRouter()

@router.post("")
def global_search(
    query: str,
    limit: int = 5,
    db: Session = Depends(get_db),
    vector_service: VectorStoreService = Depends(get_vectorstore_service)
):
    """POST /search - Global semantic search query across all repositories."""
    # Stub: query all repos (passing repo_id=0 as placeholder)
    return vector_service.search_similar_chunks(repo_id=0, query=query, limit=limit)

@router.get("/{id}")
def repository_search(
    id: int,
    query: str = Query(..., description="Semantic search query"),
    limit: int = Query(5, description="Number of results to return"),
    db: Session = Depends(get_db),
    vector_service: VectorStoreService = Depends(get_vectorstore_service)
):
    """GET /repositories/{id}/search - Semantic search query restricted to a single repository."""
    return vector_service.search_similar_chunks(repo_id=id, query=query, limit=limit)
