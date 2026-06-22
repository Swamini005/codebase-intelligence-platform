# Import all models so that Base has them registered before migrations
from backend.models.base import Base
from backend.models.user import User
from backend.models.repository import Repository
from backend.models.file import File
from backend.models.chunk import CodeChunk
from backend.models.symbol import Symbol
from backend.models.chat import ChatSession, ChatMessage
from backend.models.analysis import AnalysisResult
