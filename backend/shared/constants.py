# Global Constants for AI-Powered Codebase Intelligence Platform

DEFAULT_CHUNK_SIZE = 1000  # Characters
DEFAULT_CHUNK_OVERLAP = 200  # Characters

# Model names
DEFAULT_EMBEDDING_MODEL = "models/embedding-001"  # Google Gemini embedding
DEFAULT_LLM_MODEL = "gemini-1.5-pro"

# Storage
MAX_UPLOAD_SIZE_BYTES = 50 * 1024 * 1024  # 50MB
ALLOWED_UPLOAD_EXTENSIONS = {".zip", ".tar", ".gz"}

EXTENSION_TO_LANGUAGE: dict[str, str] = {
  ".py": "Python", ".js": "JavaScript", ".ts": "TypeScript",
  ".jsx": "JavaScript", ".tsx": "TypeScript", ".java": "Java",
  ".go": "Go", ".rs": "Rust", ".cpp": "C++", ".c": "C",
  ".h": "C/C++ Header", ".cs": "C#", ".rb": "Ruby",
  ".php": "PHP", ".swift": "Swift", ".kt": "Kotlin",
  ".md": "Markdown", ".yaml": "YAML", ".yml": "YAML",
  ".json": "JSON", ".toml": "TOML"
}

SKIP_DIRECTORIES: set[str] = {
  ".git", "node_modules", "__pycache__", ".venv", "venv",
  "env", "dist", "build", ".next", "coverage", ".pytest_cache",
  ".mypy_cache", "target", "vendor", ".idea", ".vscode"
}

BINARY_EXTENSIONS: set[str] = {
  ".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".pdf",
  ".zip", ".tar", ".gz", ".exe", ".bin", ".so", ".dylib",
  ".lock", ".woff", ".woff2", ".ttf", ".eot"
}

