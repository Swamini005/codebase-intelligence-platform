from typing import Optional

class CodebaseIntelException(Exception):
    """Base class for all Codebase Intelligence exceptions."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        self.message = message
        self.detail = detail if detail is not None else {}
        super().__init__(message)

    def __str__(self) -> str:
        return f"{self.message} | detail={self.detail}"

# GitHub Exceptions
class GitHubException(CodebaseIntelException):
    """Base exception for all GitHub-related errors."""
    pass

class RepoNotFoundException(GitHubException):
    """Raised when GitHub returns 404."""
    pass

class RepoCloneException(GitHubException):
    """Raised when git clone fails."""
    pass

class InvalidGitHubURLException(GitHubException):
    """Raised for malformed GitHub URLs."""
    pass

class RepoCloningTimeoutException(GitHubException):
    """Raised after a cloning timeout."""
    pass

# Storage Exceptions
class StorageException(CodebaseIntelException):
    """Base exception for storage-related errors."""
    pass

class FileReadException(StorageException):
    """Raised when a file cannot be read."""
    pass

# Processing / Pipeline Exceptions
class ProcessingException(CodebaseIntelException):
    """Base exception for pipeline processing errors."""
    pass

class UnsupportedFileTypeException(ProcessingException):
    """Raised for filtered/unsupported file types."""
    pass

class FileTooLargeException(ProcessingException):
    """Raised when a file exceeds MAX_FILE_SIZE_KB."""
    pass

# Backward compatibility exceptions
class PlatformException(CodebaseIntelException):
    """Base exception for the Codebase Intelligence Platform (legacy)."""
    def __init__(self, message: str, status_code: int = 500, detail: Optional[dict] = None):
        self.status_code = status_code
        super().__init__(message, detail)

class EntityNotFoundException(PlatformException):
    """Exception raised when an entity is not found (legacy)."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        super().__init__(message, status_code=404, detail=detail)

class GitIntegrationException(PlatformException):
    """Exception raised when clone or git fetch operations fail (legacy)."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        super().__init__(message, status_code=400, detail=detail)

class ParserException(PlatformException):
    """Exception raised during AST parsing failure (legacy)."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        super().__init__(message, status_code=422, detail=detail)

class EmbeddingException(PlatformException):
    """Exception raised during LLM or embedding generation (legacy)."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        super().__init__(message, status_code=502, detail=detail)

class VectorStoreException(PlatformException):
    """Exception raised during interaction with vector store (legacy)."""
    def __init__(self, message: str, detail: Optional[dict] = None):
        super().__init__(message, status_code=500, detail=detail)

