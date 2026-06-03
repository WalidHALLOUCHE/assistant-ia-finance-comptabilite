"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI provider settings: ollama (local), gemini (API), or groq (API chat).
    ai_provider: str = "ollama"

    # Ollama settings (open-source, local).
    ollama_base_url: str = "http://localhost:11434"
    ollama_model: str = "mistral"
    embedding_model: str = "nomic-embed-text"
    ollama_timeout: int = 20

    # Gemini API settings.
    gemini_api_key: Optional[str] = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_embedding_model: str = "models/gemini-embedding-001"

    # Groq API settings.
    groq_api_key: Optional[str] = None
    groq_model: str = "llama-3.3-70b-versatile"

    # Embeddings: ollama for local, gemini for full API RAG.
    # Groq does not provide embeddings for this pipeline.
    embedding_provider: str = ""

    # Vector store settings.
    vector_store_path: str = "vector_store"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    # Application settings.
    log_level: str = "INFO"
    max_tokens: int = 1500
    temperature: float = 0.7

    class Config:
        env_file = ".env"
        extra = "ignore"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ai_provider = self.ai_provider.lower()
        self.embedding_provider = self.embedding_provider.lower()

    def resolved_embedding_provider(self) -> str:
        """Return the embedding provider to use."""
        if self.embedding_provider:
            return self.embedding_provider
        if self.ai_provider == "gemini":
            return "gemini"
        return "ollama"

    @property
    def dynamic_vector_store_path(self) -> str:
        """Return a provider-specific vector store path to prevent embedding dimension mismatch."""
        return f"{self.vector_store_path}_{self.resolved_embedding_provider()}"

    def validate_ai_configuration(self) -> tuple[bool, str]:
        """Validate the selected AI provider configuration."""
        provider = self.ai_provider

        if provider == "gemini":
            if self.gemini_api_key:
                return True, f"Gemini API configured ({self.gemini_model})"
            return False, "GEMINI_API_KEY is missing. Add it to .env or use AI_PROVIDER=ollama."

        if provider == "groq":
            if self.groq_api_key:
                return True, f"Groq API configured ({self.groq_model})"
            return False, "GROQ_API_KEY is missing. Add it to .env or use AI_PROVIDER=ollama."

        if provider != "ollama":
            return False, "AI_PROVIDER must be one of: ollama, gemini, groq."

        import requests

        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return True, f"Ollama is running at {self.ollama_base_url}"
        except Exception:
            pass

        return False, (
            f"Ollama not accessible at {self.ollama_base_url}. "
            "Please ensure Ollama is installed and running. "
            "Download from: https://ollama.ai"
        )

    def get_project_root(self) -> Path:
        """Get the root directory of the project."""
        return Path(__file__).parent.parent


settings = Settings()
