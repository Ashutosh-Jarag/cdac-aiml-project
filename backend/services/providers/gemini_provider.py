"""
Gemini Provider Module
----------------------
This module defines the `GeminiProvider` class, which wraps Google's GenAI Client SDK 
for interacting with Gemini models (specifically `gemini-3-flash-preview`).

Key functionality:
  - Synchronous content generation (`generate`).
  - Streaming content generation (`stream_generate`).
  - Optional system prompt concatenation with user input prompts.
"""

from typing import Generator, Optional
from google import genai


class GeminiProvider:
    """
    Provider wrapper class for interacting with Google Gemini models via Google GenAI SDK.
    """

    def __init__(self, api_key: str):
        """
        Initializes the Gemini provider with the provided API key.

        Args:
            api_key (str): Authentication API key string for Google Gemini services.

        Returns:
            None
        """
        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-3-flash-preview"

    def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> str:
        """
        Generates a complete textual response synchronously using Gemini.

        Args:
            prompt (str): Main user prompt text.
            system_prompt (Optional[str]): Optional system prompt guidelines to prepended to prompt.

        Returns:
            str: Generated output text response.
        """
        if system_prompt:
            prompt = f"""
{system_prompt}

{prompt}
"""

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
        )

        return response.text

    # ----------------------------
    # Streaming Support
    # ----------------------------

    def stream_generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
    ) -> Generator[str, None, None]:
        """
        Streams generated text response chunks incrementally from Gemini.

        Args:
            prompt (str): Main user prompt text.
            system_prompt (Optional[str]): Optional system prompt guidelines to prepended to prompt.

        Yields:
            str: Individual generated text chunks as they arrive.
        """
        if system_prompt:
            prompt = f"""
{system_prompt}

{prompt}
"""

        response = self.client.models.generate_content_stream(
            model=self.model,
            contents=prompt,
        )

        for chunk in response:
            if chunk.text:
                yield chunk.text