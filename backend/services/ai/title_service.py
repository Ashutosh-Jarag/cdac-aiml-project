"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `TitleService` class, responsible for generating short, concise conversation titles 
for chat sessions based on the user's initial question.

Key functionality:
  - generate(): Formats a title-generation prompt with formatting constraints (max 5 words, no punctuation/quotes),
                invokes the requested LLM provider via `ai_manager`, logs the output, and returns the generated title string.

Exports:
  - title_service: Singleton instance of `TitleService` for application-wide title generation operations.
"""

from typing import Any, Optional

from app.core.ai_manager import ai_manager
from app.core.logger import logger


class TitleService:
    """
    Service class responsible for auto-generating concise titles for chat sessions based on user input.
    """

    def generate(
        self,
        question: str,
        provider: str = "gemini",
        api_key: Optional[str] = None,
    ) -> str:
        """
        Generates a short chat session title (maximum 5 words) based on the provided user question.

        Args:
            question (str): The initial question or prompt provided by the user.
            provider (str, optional): Identifier of the AI model provider to use. Defaults to "gemini".
            api_key (str, optional): Custom API key for provider authentication. Defaults to None.

        Returns:
            str: The cleaned, generated title string.
        """
        llm = ai_manager.get_provider(
            provider,
            api_key,
        )

        prompt = f"""
Generate a short chat title.

Rules:
- Maximum 5 words
- No punctuation
- No quotes
- Return ONLY the title

Question:

{question}
"""

        title = llm.generate(prompt).strip()

        logger.info(f"Generated title: {title}")

        return title


# Global singleton instance of TitleService
title_service = TitleService()