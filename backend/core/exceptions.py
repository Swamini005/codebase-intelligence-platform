class PlatformException(Exception):
    """Base exception for the Codebase Intelligence Platform."""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class EntityNotFoundException(PlatformException):
    """Exception raised when an entity (User, Repo, File, etc.) is not found."""
    def __init__(self, message: str):
        super().__init__(message, status_code=404)

class GitIntegrationException(PlatformException):
    """Exception raised when clone or git fetch operations fail."""
    def __init__(self, message: str):
        super().__init__(message, status_code=400)

class ParserException(PlatformException):
    """Exception raised during AST parsing failure."""
    def __init__(self, message: str):
        super().__init__(message, status_code=422)

class EmbeddingException(PlatformException):
    """Exception raised during LLM or embedding generation."""
    def __init__(self, message: str):
        super().__init__(message, status_code=502)

class VectorStoreException(PlatformException):
    """Exception raised during interaction with vector store (Chroma)."""
    def __init__(self, message: str):
        super().__init__(message, status_code=500)
