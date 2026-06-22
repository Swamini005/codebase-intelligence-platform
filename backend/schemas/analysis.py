from pydantic import BaseModel
from typing import Any, Dict, List
from backend.shared.enums import AnalysisType

class AnalysisResultResponse(BaseModel):
    id: int
    repository_id: int
    analysis_type: AnalysisType
    result_json: Dict[str, Any]

    class Config:
        from_attributes = True

class DependencyNode(BaseModel):
    id: str
    label: str
    type: str

class DependencyEdge(BaseModel):
    source: str
    target: str
    type: str = "dependency"

class DependencyGraphResponse(BaseModel):
    repository_id: int
    nodes: List[DependencyNode]
    edges: List[DependencyEdge]

class ArchitectureModule(BaseModel):
    name: str
    files: List[str]
    dependencies: List[str]

class ArchitectureResponse(BaseModel):
    repository_id: int
    modules: List[ArchitectureModule]
