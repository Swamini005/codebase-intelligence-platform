from abc import ABC, abstractmethod
from typing import List, Dict, Any

class ChunkingService(ABC):
    @abstractmethod
    def chunk_file(self, content: str, file_path: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        """Split source code file content into logical/structural chunks."""
        pass


class ChunkingServiceImpl(ChunkingService):
    def chunk_file(self, content: str, file_path: str, chunk_size: int = 1000) -> List[Dict[str, Any]]:
        # Stub implementation doing simplistic line-based chunking
        lines = content.splitlines()
        chunks = []
        # Return a single chunk for simplicity in mock
        chunks.append({
            "chunk_text": content,
            "start_line": 1,
            "end_line": len(lines) if lines else 1
        })
        return chunks
