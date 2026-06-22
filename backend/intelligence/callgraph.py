from abc import ABC, abstractmethod
from typing import Dict, Any

class BaseCallGraphBuilder(ABC):
    @abstractmethod
    def build_call_graph(self, repository_path: str) -> Dict[str, Any]:
        """Statically traces function call references to build a call graph."""
        pass

class StaticCallGraphBuilder(BaseCallGraphBuilder):
    """Stub static call graph builder."""
    def build_call_graph(self, repository_path: str) -> Dict[str, Any]:
        # Return mock call graph
        return {
            "nodes": [
                {"id": "main.start", "label": "main:start()", "type": "function"},
                {"id": "services.repository.RepositoryService.index", "label": "RepositoryService:index()", "type": "method"},
                {"id": "data_access.repository_dao.repository_dao.get", "label": "repository_dao:get()", "type": "method"}
            ],
            "edges": [
                {"source": "main.start", "target": "services.repository.RepositoryService.index"},
                {"source": "services.repository.RepositoryService.index", "target": "data_access.repository_dao.repository_dao.get"}
            ]
        }
