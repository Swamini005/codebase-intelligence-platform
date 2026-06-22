import os
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    PROJECT_NAME: str = "Codebase Intelligence Platform"
    API_V1_STR: str = "/api/v1"
    
    # Database Settings
    DATABASE_URL: str = Field(default="postgresql://postgres:postgres@localhost:5432/codebase_intel")
    
    # Gemini AI Settings
    GEMINI_API_KEY: str = Field(default="")
    
    # Vector Database Settings
    CHROMA_HOST: str = Field(default="localhost")
    CHROMA_PORT: int = Field(default=8000)
    
    # AWS Storage Settings (Future EC2/S3)
    AWS_ACCESS_KEY: str = Field(default="")
    AWS_SECRET_KEY: str = Field(default="")
    AWS_S3_BUCKET: str = Field(default="codebase-intel-artifacts")
    
    # Local Storage Settings
    STORAGE_DIR: str = Field(default="./storage_data")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()
