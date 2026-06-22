from backend.providers.llm.base import LlmProvider

class LLMGenerator:
    def __init__(self, llm_provider: LlmProvider):
        self.llm_provider = llm_provider

    def generate(self, prompt: str) -> str:
        """Call LLM provider to render completion answer."""
        return self.llm_provider.generate_response(prompt)
