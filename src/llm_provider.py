"""LLM provider abstraction layer using Ollama (open-source, local)."""

import os
from typing import Optional
from src.config import settings


class LLMProvider:
    """Abstraction layer for Ollama LLM provider (open-source, local)."""

    def __init__(self):
        """Initialize the LLM provider."""
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate that Ollama is properly configured."""
        is_valid, message = settings.validate_ai_configuration()
        if not is_valid:
            raise ValueError(message)

    def get_chat_model(self):
        """Get the chat model using Ollama."""
        from langchain_ollama import ChatOllama

        return ChatOllama(
            model=settings.ollama_model,
            base_url=settings.ollama_base_url,
            temperature=settings.temperature,
            num_ctx=2048,
            num_predict=min(settings.max_tokens, 512),
            timeout=settings.ollama_timeout,
        )

    def get_embeddings_model(self):
        """Get the embeddings model using Ollama."""
        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    @staticmethod
    def is_api_available() -> bool:
        """Check if Ollama is available."""
        is_valid, _ = settings.validate_ai_configuration()
        return is_valid

    @staticmethod
    def get_provider_info() -> dict:
        """Get information about configured provider."""
        is_valid, message = settings.validate_ai_configuration()
        return {
            "available": is_valid,
            "provider": "Ollama (Open-Source, Local)",
            "model": settings.ollama_model,
            "embedding_model": settings.embedding_model,
            "base_url": settings.ollama_base_url,
            "message": message,
        }
