class PromptBuilder:
    def create_rag_prompt(self, context: str, user_query: str) -> str:
        """Create structured RAG prompt containing reference context and query."""
        prompt = (
            "You are an expert AI software developer assistant. Answer the user's question about the codebase\n"
            "using only the provided context source blocks. If the code is not mentioned in the context or if you\n"
            "cannot find the answer, state that you do not know. Do not guess.\n\n"
            "=== Codebase Context ===\n"
            f"{context}\n\n"
            "=== User Question ===\n"
            f"{user_query}\n\n"
            "Answer:"
        )
        return prompt
