from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from backend.schemas.chat import ChatRequest, ChatResponse
from backend.rag.retriever import Retriever
from backend.rag.context import ContextBuilder
from backend.rag.prompt import PromptBuilder
from backend.rag.generator import LLMGenerator

class ChatService(ABC):
    @abstractmethod
    def process_chat_message(self, db: Session, chat_req: ChatRequest) -> ChatResponse:
        """Processes message, retrieves context, queries LLM, logs session history, and returns response."""
        pass


class ChatServiceImpl(ChatService):
    def __init__(
        self,
        retriever: Retriever,
        context_builder: ContextBuilder,
        prompt_builder: PromptBuilder,
        generator: LLMGenerator
    ):
        self.retriever = retriever
        self.context_builder = context_builder
        self.prompt_builder = prompt_builder
        self.generator = generator

    def process_chat_message(self, db: Session, chat_req: ChatRequest) -> ChatResponse:
        from backend.data_access.chat_dao import chat_dao
        from backend.shared.enums import ChatMessageRole
        
        # 1. Create or fetch chat session
        session_id = chat_req.session_id
        if not session_id:
            session = chat_dao.create_session(db, chat_req.repository_id)
            session_id = session.id
            
        # Log user message
        chat_dao.add_message(db, session_id, ChatMessageRole.USER, chat_req.message)
        
        # 2. Retrieve chunks
        chunks = self.retriever.retrieve_relevant_chunks(chat_req.repository_id, chat_req.message)
        
        # 3. Build context & prompt
        context = self.context_builder.build_context(chunks)
        prompt = self.prompt_builder.create_rag_prompt(context, chat_req.message)
        
        # 4. Generate response
        response_text = self.generator.generate(prompt)
        
        # Log assistant response
        chat_dao.add_message(db, session_id, ChatMessageRole.ASSISTANT, response_text)
        
        sources = [c.get("metadata", {}).get("file_path", "unknown") for c in chunks]
        
        return ChatResponse(
            session_id=session_id,
            response=response_text,
            sources=list(set(sources))
        )
