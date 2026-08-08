from app.core.config import settings
from services.providers.gemini_provider import GeminiProvider


class AIManager:

    def get_provider(
        self,
        provider: str | None = None,
        api_key: str | None = None,
    ):

        provider = (provider or "gemini").strip().lower()

        if provider == "gemini":
            return GeminiProvider(
                api_key or settings.GEMINI_API_KEY
            )

        raise ValueError(f"Unsupported provider: {provider}")


ai_manager = AIManager()