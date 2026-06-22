from typing import List
from backend.providers.embeddings.base import EmbeddingProvider

class SentenceTransformersEmbeddingProvider(EmbeddingProvider):
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.model_name = model_name
        # In a real implementation, initialize sentence_transformers.SentenceTransformer

    def embed_text(self, text: str) -> List[float]:
        # Return mock 384-dimensional vector (standard for MiniLM)
        return [0.05] * 384

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [[0.05] * 384 for _ in texts]
