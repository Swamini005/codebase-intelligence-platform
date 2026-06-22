from abc import ABC, abstractmethod
from typing import List, Dict, Any

class LlmProvider(ABC):
    @abstractmethod
    def generate_response(self, prompt: str, system_instruction: str = None) -> str:
        """Generate response from LLM given a prompt."""
        pass

    @abstractmethod
    def chat(self, messages: List[Dict[str, str]]) -> str:
        """Chat session runner."""
        pass
