from typing import Generator
from fastapi import Depends
from sqlalchemy.orm import Session
from backend.db.session import get_db

# Providers
from backend.providers.embeddings.gemini import GeminiEmbeddingProvider
from backend.providers.llm.gemini import GeminiLlmProvider
from backend.providers.parser.python import PythonParser
from backend.vectorstore.chroma import ChromaVectorStore

# RAG Subsystems
from backend.rag.retriever import Retriever
from backend.rag.context import ContextBuilder
from backend.rag.prompt import PromptBuilder
from backend.rag.generator import LLMGenerator

# Services
from backend.services.repository import RepositoryService, RepositoryServiceImpl
from backend.services.chat import ChatService, ChatServiceImpl
from backend.services.vectorstore import VectorStoreService, VectorStoreServiceImpl
from backend.services.architecture import ArchitectureService, ArchitectureServiceImpl
from backend.intelligence.architecture import ArchitectureAnalyzer
from backend.intelligence.dependencies import StaticDependencyAnalyzer

def get_repository_service() -> RepositoryService:
    return RepositoryServiceImpl()

def get_vectorstore_service() -> VectorStoreService:
    chroma_store = ChromaVectorStore()
    return VectorStoreServiceImpl(chroma_store)

def get_chat_service() -> ChatService:
    chroma_store = ChromaVectorStore()
    vectorstore_service = VectorStoreServiceImpl(chroma_store)
    retriever = Retriever(vectorstore_service)
    context_builder = ContextBuilder()
    prompt_builder = PromptBuilder()
    
    llm_provider = GeminiLlmProvider()
    generator = LLMGenerator(llm_provider)
    
    return ChatServiceImpl(retriever, context_builder, prompt_builder, generator)

def get_architecture_service() -> ArchitectureService:
    arch_analyzer = ArchitectureAnalyzer()
    dep_analyzer = StaticDependencyAnalyzer()
    return ArchitectureServiceImpl(arch_analyzer, dep_analyzer)
