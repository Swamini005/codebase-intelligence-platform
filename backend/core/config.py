from typing import Optional, List
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # App
    APP_NAME: str = "Codebase Intelligence Platform"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str  # from .env

    # GitHub
    GITHUB_TOKEN: Optional[str] = None  # for private repos and higher rate limits

    # Storage
    STORAGE_BACKEND: str = "local"  # "local" or "s3"
    REPOS_BASE_DIR: str = "./repos"  # where cloned repos are stored on disk

    # File filtering
    SUPPORTED_EXTENSIONS: list[str] = [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".java", ".go",
        ".rs", ".cpp", ".c", ".h", ".cs", ".rb", ".php",
        ".swift", ".kt", ".md", ".yaml", ".yml", ".json", ".toml"
    ]
    MAX_FILE_SIZE_KB: int = 500
    BINARY_CHECK_BYTES: int = 8000

    # Chunking
    DEFAULT_CHUNK_SIZE: int = 1500
    DEFAULT_CHUNK_OVERLAP: int = 200

    # ChromaDB
    CHROMA_HOST: str = "localhost"
    CHROMA_PORT: int = 8001
    CHROMA_COLLECTION_PREFIX: str = "repo_"

    # Embeddings
    EMBEDDING_PROVIDER: str = "sentence_transformers"  # or "gemini"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # LLM
    LLM_PROVIDER: str = "gemini"
    LLM_MODEL: str = "gemini-pro"
    GEMINI_API_KEY: Optional[str] = None

    # AWS Storage (kept for compatibility with storage/s3.py stubs)
    AWS_ACCESS_KEY: Optional[str] = None
    AWS_SECRET_KEY: Optional[str] = None
    AWS_S3_BUCKET: str = "codebase-intel-artifacts"

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    # Compatibility properties for older code references
    @property
    def PROJECT_NAME(self) -> str:
        return self.APP_NAME

    @property
    def API_V1_STR(self) -> str:
        return self.API_V1_PREFIX

    @property
    def STORAGE_DIR(self) -> str:
        return self.REPOS_BASE_DIR

@lru_cache
def get_settings() -> Settings:
    return Settings()

settings = get_settings()

