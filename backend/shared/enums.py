from enum import Enum

class RepositoryStatus(str, Enum):
    PENDING = "PENDING"
    INDEXING = "INDEXING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    
    # New statuses for ingestion pipeline
    processing = "processing"
    completed = "completed"
    failed = "failed"
    pending = "pending"


class AnalysisType(str, Enum):
    ARCHITECTURE = "ARCHITECTURE"
    DEPENDENCY = "DEPENDENCY"
    CALLGRAPH = "CALLGRAPH"
    ML_ANALYTICS = "ML_ANALYTICS"

class FileLanguage(str, Enum):
    PYTHON = "PYTHON"
    JAVASCRIPT = "JAVASCRIPT"
    TYPESCRIPT = "TYPESCRIPT"
    UNKNOWN = "UNKNOWN"

class SymbolType(str, Enum):
    FUNCTION = "FUNCTION"
    CLASS = "CLASS"
    INTERFACE = "INTERFACE"
    ENUM = "ENUM"
    VARIABLE = "VARIABLE"

class ChatMessageRole(str, Enum):
    USER = "USER"
    SYSTEM = "SYSTEM"
    ASSISTANT = "ASSISTANT"
