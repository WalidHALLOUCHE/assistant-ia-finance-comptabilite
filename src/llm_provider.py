"""LLM provider abstraction layer for local and API models."""

from src.config import settings


class LLMProvider:
    """Abstraction layer for Ollama, Gemini, and Groq providers."""

    def __init__(self):
        """Initialize the LLM provider."""
        self._validate_configuration()

    def _validate_configuration(self) -> None:
        """Validate that the selected provider is properly configured."""
        is_valid, message = settings.validate_ai_configuration()
        if not is_valid:
            raise ValueError(message)

    def get_chat_model(self):
        """Get the chat model for the configured provider."""
        provider = settings.ai_provider

        if provider == "gemini":
            from langchain_google_genai import ChatGoogleGenerativeAI

            return ChatGoogleGenerativeAI(
                model=settings.gemini_model,
                google_api_key=settings.gemini_api_key,
                temperature=settings.temperature,
                max_output_tokens=settings.max_tokens,
            )

        if provider == "groq":
            from langchain_groq import ChatGroq

            return ChatGroq(
                model=settings.groq_model,
                groq_api_key=settings.groq_api_key,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
            )

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
        """Get the embeddings model for the configured embedding provider."""
        embedding_provider = settings.resolved_embedding_provider()

        if embedding_provider == "gemini":
            if not settings.gemini_api_key:
                raise ValueError("GEMINI_API_KEY is required for EMBEDDING_PROVIDER=gemini.")

            from langchain_google_genai import GoogleGenerativeAIEmbeddings

            return GoogleGenerativeAIEmbeddings(
                model=settings.gemini_embedding_model,
                google_api_key=settings.gemini_api_key,
            )

        if embedding_provider != "ollama":
            raise ValueError("EMBEDDING_PROVIDER must be one of: ollama, gemini.")

        from langchain_ollama import OllamaEmbeddings

        return OllamaEmbeddings(
            model=settings.embedding_model,
            base_url=settings.ollama_base_url,
        )

    @staticmethod
    def is_api_available() -> bool:
        """Check if the selected provider is available."""
        is_valid, _ = settings.validate_ai_configuration()
        return is_valid

    @staticmethod
    def get_provider_info() -> dict:
        """Get information about the configured provider."""
        is_valid, message = settings.validate_ai_configuration()
        embedding_provider = settings.resolved_embedding_provider()

        model_by_provider = {
            "ollama": settings.ollama_model,
            "gemini": settings.gemini_model,
            "groq": settings.groq_model,
        }
        embedding_model_by_provider = {
            "ollama": settings.embedding_model,
            "gemini": settings.gemini_embedding_model,
        }

        return {
            "available": is_valid,
            "provider": settings.ai_provider,
            "model": model_by_provider.get(settings.ai_provider),
            "embedding_provider": embedding_provider,
            "embedding_model": embedding_model_by_provider.get(embedding_provider),
            "base_url": settings.ollama_base_url if settings.ai_provider == "ollama" else None,
            "message": message,
        }
