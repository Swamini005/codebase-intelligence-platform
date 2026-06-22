from abc import ABC, abstractmethod
from typing import List
from backend.providers.embeddings.base import EmbeddingProvider

class EmbeddingService(ABC):
    @abstractmethod
    def generate_chunk_embeddings(self, chunks: List[str]) -> List[List[float]]:
        """Generates embeddings for code chunks."""
        pass


class EmbeddingServiceImpl(EmbeddingService):
    def __init__(self, provider: EmbeddingProvider):
        self.provider = provider

    def generate_chunk_embeddings(self, chunks: List[str]) -> List[List[float]]:
        return self.provider.embed_batch(chunks)
