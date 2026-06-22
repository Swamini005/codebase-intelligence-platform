from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseParser(ABC):
    @abstractmethod
    def parse_file(self, content: str, file_path: str) -> Dict[str, Any]:
        """Parses a file's content and returns structured code intelligence nodes.
        
        Returns:
            Dict containing metadata, symbols, imports, and documentation chunks.
        """
        pass
