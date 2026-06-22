from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseDependencyAnalyzer(ABC):
    @abstractmethod
    def analyze_dependencies(self, repository_path: str) -> Dict[str, Any]:
        """Scans the repository path to build import-level dependencies.
        
        Returns a dict of nodes and links/edges suitable for graphing.
        """
        pass

class StaticDependencyAnalyzer(BaseDependencyAnalyzer):
    """NetworkX/AST based static dependency analyzer stub."""
    def analyze_dependencies(self, repository_path: str) -> Dict[str, Any]:
        # Return mock nodes and edges structure
        return {
            "nodes": [
                {"id": "main.py", "label": "main.py", "type": "module"},
                {"id": "core/config.py", "label": "config.py", "type": "module"},
                {"id": "db/session.py", "label": "session.py", "type": "module"}
            ],
            "edges": [
                {"source": "main.py", "target": "core/config.py", "type": "dependency"},
                {"source": "main.py", "target": "db/session.py", "type": "dependency"}
            ]
        }
