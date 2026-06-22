from abc import ABC, abstractmethod
from typing import List, Dict, Any
from backend.rag.retriever import Retriever

class RetrievalService(ABC):
    @abstractmethod
    def retrieve_context(self, repository_id: int, query: str) -> List[Dict[str, Any]]:
        """Fetch context snippets using retrieval pipeline."""
        pass


class RetrievalServiceImpl(RetrievalService):
    def __init__(self, retriever: Retriever):
        self.retriever = retriever

    def retrieve_context(self, repository_id: int, query: str) -> List[Dict[str, Any]]:
        return self.retriever.retrieve_relevant_chunks(repository_id, query)
