from typing import Dict, Any
from backend.providers.parser.base import BaseParser

class TypeScriptParser(BaseParser):
    def parse_file(self, content: str, file_path: str) -> Dict[str, Any]:
        """TypeScript parser stub (future extension using tree-sitter or node-ts-morph)."""
        # Return skeleton structure
        return {
            "language": "typescript",
            "classes": [],
            "interfaces": [],
            "functions": [],
            "imports": [],
            "error": None
        }
