from app.core.ai_manager import ai_manager
from app.core.logger import logger


class TitleService:

    def generate(
        self,
        question: str,
        provider="gemini",
        api_key=None,
    ):

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


title_service = TitleService()