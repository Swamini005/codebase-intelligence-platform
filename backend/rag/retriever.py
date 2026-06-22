from typing import List, Dict, Any
from backend.services.vectorstore import VectorStoreService

class Retriever:
    def __init__(self, vectorstore_service: VectorStoreService):
        self.vectorstore_service = vectorstore_service

    def retrieve_relevant_chunks(self, repository_id: int, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        """Query semantic search to obtain context snippets."""
        return self.vectorstore_service.search_similar_chunks(repository_id, query, limit)
