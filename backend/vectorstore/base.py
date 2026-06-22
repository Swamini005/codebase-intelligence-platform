from abc import ABC, abstractmethod
from typing import List, Dict, Any

class VectorStore(ABC):
    @abstractmethod
    def add_documents(self, documents: List[str], metadatas: List[Dict[str, Any]], ids: List[str]) -> bool:
        """Adds documents/chunks and metadata to the vector database."""
        pass

    @abstractmethod
    def similarity_search(self, query: str, k: int = 4, filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Returns documents similar to the query."""
        pass

    @abstractmethod
    def delete_documents(self, ids: List[str]) -> bool:
        """Deletes documents from the vector database by ID."""
        pass
