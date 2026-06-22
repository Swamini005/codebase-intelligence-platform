from typing import List, Dict, Any

class ContextBuilder:
    def build_context(self, chunks: List[Dict[str, Any]]) -> str:
        """Formulate string blocks representing matching chunks for prompt injection."""
        context_blocks = []
        for idx, chunk in enumerate(chunks):
            doc = chunk.get("document", "")
            meta = chunk.get("metadata", {})
            file_path = meta.get("file_path", "unknown_file")
            start = meta.get("start_line", 0)
            end = meta.get("end_line", 0)
            
            block = f"--- Source File: {file_path} (Lines {start}-{end}) ---\n{doc}\n"
            context_blocks.append(block)
            
        return "\n".join(context_blocks)
