"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the AI manager service component responsible for provider resolution and instantiation.
It acts as a factory for instantiating specific AI model integration providers (such as GeminiProvider)
based on requested provider strings and API key configurations.

Classes & Objects:
  - AIManager: Factory class for validating and returning AI provider instances.
  - ai_manager: Pre-instantiated singleton instance of AIManager for convenient app-wide usage.
"""

from app.core.config import settings
from services.providers.gemini_provider import GeminiProvider


class AIManager:
    """
    Factory class responsible for dynamically resolving and instantiating AI provider services.
    """

    def get_provider(
        self,
        provider: str | None = None,
        api_key: str | None = None,
    ):
        """
        Resolves the requested AI provider string and returns an initialized provider instance.

        Args:
            provider (str | None): Target provider identifier (e.g., 'gemini'). 
                                   Defaults to "gemini" if None or empty.
            api_key (str | None): Custom API key to override system defaults. 
                                  If None, falls back to `settings.GEMINI_API_KEY`.

        Returns:
            GeminiProvider: An initialized instance of the requested provider service.

        Raises:
            ValueError: If the requested provider string is not supported by the system.
        """
        provider = (provider or "gemini").strip().lower()

        if provider == "gemini":
            return GeminiProvider(
                api_key or settings.GEMINI_API_KEY
            )

        raise ValueError(f"Unsupported provider: {provider}")


# Global singleton instance of AIManager
ai_manager = AIManager()