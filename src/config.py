"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # AI provider settings: ollama (local), gemini (API), or groq (API chat).
    ai_provider: str = os.getenv("AI_PROVIDER", "ollama").lower()

    # Ollama settings (open-source, local).
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "20"))

    # Gemini API settings.
    gemini_api_key: Optional[str] = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    gemini_embedding_model: str = os.getenv("GEMINI_EMBEDDING_MODEL", "models/embedding-001")

    # Groq API settings.
    groq_api_key: Optional[str] = os.getenv("GROQ_API_KEY")
    groq_model: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

    # Embeddings: ollama for local, gemini for full API RAG.
    # Groq does not provide embeddings for this pipeline.
    embedding_provider: str = os.getenv("EMBEDDING_PROVIDER", "").lower()

    # Vector store settings.
    vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "vector_store")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Application settings.
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1500"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))

    class Config:
        env_file = ".env"
        extra = "ignore"

    def resolved_embedding_provider(self) -> str:
        """Return the embedding provider to use."""
        if self.embedding_provider:
            return self.embedding_provider
        if self.ai_provider == "gemini":
            return "gemini"
        return "ollama"

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
