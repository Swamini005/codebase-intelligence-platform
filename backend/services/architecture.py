from abc import ABC, abstractmethod
from typing import Dict, Any
from sqlalchemy.orm import Session
from backend.intelligence.architecture import BaseArchitectureAnalyzer
from backend.intelligence.dependencies import BaseDependencyAnalyzer

class ArchitectureService(ABC):
    @abstractmethod
    def get_architecture_overview(self, db: Session, repo_id: int) -> Dict[str, Any]:
        """Generate high-level components and architecture outline."""
        pass

    @abstractmethod
    def get_dependency_graph(self, db: Session, repo_id: int) -> Dict[str, Any]:
        """Generate full static module dependency graph nodes and links."""
        pass


class ArchitectureServiceImpl(ArchitectureService):
    def __init__(self
        , arch_analyzer: BaseArchitectureAnalyzer
        , dep_analyzer: BaseDependencyAnalyzer
    ):
        self.arch_analyzer = arch_analyzer
        self.dep_analyzer = dep_analyzer

    def get_architecture_overview(self, db: Session, repo_id: int) -> Dict[str, Any]:
        # Return mock analysis calling analyzer
        # In full impl, this would fetch repository path from db
        return self.arch_analyzer.analyze_architecture("/dummy/repo/path")

    def get_dependency_graph(self, db: Session, repo_id: int) -> Dict[str, Any]:
        # Return mock dependency graph calling analyzer
        return self.dep_analyzer.analyze_dependencies("/dummy/repo/path")
