from abc import ABC, abstractmethod
from typing import List, Dict, Any
from backend.vectorstore.base import VectorStore

class VectorStoreService(ABC):
    @abstractmethod
    def index_chunks(self, chunks: List[Dict[str, Any]], repo_id: int) -> bool:
        """Stores code chunks into the vector database collection."""
        pass

    @abstractmethod
    def search_similar_chunks(self, repo_id: int, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Queries the vector database for matching chunks."""
        pass


class VectorStoreServiceImpl(VectorStoreService):
    def __init__(self, vectorstore: VectorStore):
        self.vectorstore = vectorstore

    def index_chunks(self, chunks: List[Dict[str, Any]], repo_id: int) -> bool:
        documents = [c["chunk_text"] for c in chunks]
        metadatas = [{"repository_id": repo_id, "start_line": c["start_line"], "end_line": c["end_line"]} for c in chunks]
        ids = [f"repo_{repo_id}_chunk_{i}" for i in range(len(chunks))]
        return self.vectorstore.add_documents(documents, metadatas, ids)

    def search_similar_chunks(self, repo_id: int, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        filter_dict = {"repository_id": repo_id}
        return self.vectorstore.similarity_search(query, k=limit, filter=filter_dict)
