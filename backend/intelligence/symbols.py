from abc import ABC, abstractmethod
from typing import List, Dict, Any
from backend.shared.enums import SymbolType

class BaseSymbolExtractor(ABC):
    @abstractmethod
    def extract_symbols(self, file_content: str, file_path: str) -> List[Dict[str, Any]]:
        """Extract functions, classes, interfaces, enums, or variables from file content.
        
        Returns a list of dictionaries with structure matching the Symbol model/schema.
        """
        pass

class ASTSymbolExtractor(BaseSymbolExtractor):
    """AST-based symbol extractor stub."""
    def extract_symbols(self, file_content: str, file_path: str) -> List[Dict[str, Any]]:
        # TODO: Implement Python AST / Tree-sitter extraction logic.
        # Returning dummy symbols for contract validation.
        if file_path.endswith(".py"):
            return [
                {
                    "name": "PlatformException",
                    "symbol_type": SymbolType.CLASS,
                    "start_line": 1,
                    "end_line": 5,
                    "metadata_json": {"methods": ["__init__"]}
                },
                {
                    "name": "get_logger",
                    "symbol_type": SymbolType.FUNCTION,
                    "start_line": 3,
                    "end_line": 12,
                    "metadata_json": {"parameters": ["name"]}
                }
            ]
        return []
