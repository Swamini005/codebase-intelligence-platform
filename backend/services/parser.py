from abc import ABC, abstractmethod
from typing import Dict, Any, List
from backend.models.file import File

class ParserService(ABC):
    @abstractmethod
    def parse_repository_files(self, repo_path: str) -> List[Dict[str, Any]]:
        """Parses files in a directory and returns parsed code metadata."""
        pass

    @abstractmethod
    def get_supported_languages(self) -> List[str]:
        """Returns list of supported languages."""
        pass


class ParserServiceImpl(ParserService):
    def parse_repository_files(self, repo_path: str) -> List[Dict[str, Any]]:
        # Stub implementation returning mock results
        return [
            {
                "path": "main.py",
                "content": "def hello():\n    print('world')",
                "language": "PYTHON",
                "size": 36,
                "symbols": [
                    {"name": "hello", "symbol_type": "FUNCTION", "start_line": 1, "end_line": 2}
                ]
            }
        ]

    def get_supported_languages(self) -> List[str]:
        return ["PYTHON", "JAVASCRIPT", "TYPESCRIPT"]
