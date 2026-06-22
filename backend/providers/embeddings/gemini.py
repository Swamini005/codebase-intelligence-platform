from typing import List
from backend.providers.embeddings.base import EmbeddingProvider
from backend.core.config import settings

class GeminiEmbeddingProvider(EmbeddingProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        # In a real implementation, initialize google.generativeai or google-genai client

    def embed_text(self, text: str) -> List[float]:
        # Return mock 768-dimensional vector (or similar Gemini dimensions)
        return [0.1] * 768

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [[0.1] * 768 for _ in texts]
