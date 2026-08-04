from app.core.config import settings


class AIManager:

    def get_provider(
        self,
        provider: str | None = None,
        api_key: str | None = None,
    ):

        provider = provider or settings.DEFAULT_AI_PROVIDER

        if provider == "gemini":
            from services.gemini_service import GeminiService

            return GeminiService(
                api_key=api_key or settings.GEMINI_API_KEY
            )

        raise ValueError(f"Unsupported AI Provider: {provider}")


ai_manager = AIManager()