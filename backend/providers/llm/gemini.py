from typing import List, Dict
from backend.providers.llm.base import LlmProvider
from backend.core.config import settings

class GeminiLlmProvider(LlmProvider):
    def __init__(self, model_name: str = "gemini-1.5-pro"):
        self.model_name = model_name
        self.api_key = settings.GEMINI_API_KEY
        # In a real implementation, initialize google.generativeai or google-genai client

    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        # Stub response
        return f"Mocked LLM Response for prompt: {prompt[:30]}..."

    def chat(self, messages: List[Dict[str, str]]) -> str:
        # Stub response
        last_msg = messages[-1]["content"] if messages else ""
        return f"Mocked LLM chat reply to: '{last_msg}'"
