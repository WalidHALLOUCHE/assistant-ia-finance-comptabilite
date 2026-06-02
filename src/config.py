"""Configuration management for the application."""

import os
from pathlib import Path
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # LLM settings (Ollama - open-source, local)
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    ollama_model: str = os.getenv("OLLAMA_MODEL", "mistral")
    embedding_model: str = os.getenv("EMBEDDING_MODEL", "nomic-embed-text")

    # Vector store settings
    vector_store_path: str = os.getenv("VECTOR_STORE_PATH", "vector_store")
    chunk_size: int = int(os.getenv("CHUNK_SIZE", "1000"))
    chunk_overlap: int = int(os.getenv("CHUNK_OVERLAP", "200"))

    # Application settings
    log_level: str = os.getenv("LOG_LEVEL", "INFO")
    max_tokens: int = int(os.getenv("MAX_TOKENS", "1500"))
    temperature: float = float(os.getenv("TEMPERATURE", "0.7"))
    ollama_timeout: int = int(os.getenv("OLLAMA_TIMEOUT", "20"))

    class Config:
        env_file = ".env"
        extra = "ignore"

    def validate_ai_configuration(self) -> tuple[bool, str]:
        """Validate that Ollama is accessible."""
        import requests
        try:
            response = requests.get(f"{self.ollama_base_url}/api/tags", timeout=5)
            if response.status_code == 200:
                return True, f"✅ Ollama is running at {self.ollama_base_url}"
        except Exception:
            pass
        return False, (
            f"❌ Ollama not accessible at {self.ollama_base_url}. "
            "Please ensure Ollama is installed and running. "
            "Download from: https://ollama.ai"
        )

    def get_project_root(self) -> Path:
        """Get the root directory of the project."""
        return Path(__file__).parent.parent


settings = Settings()
