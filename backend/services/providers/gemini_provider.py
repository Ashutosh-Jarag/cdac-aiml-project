from google import genai


class GeminiProvider:

    def __init__(self, api_key: str):

        self.client = genai.Client(
            api_key=api_key
        )

        self.model = "gemini-2.5-flash"

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
    ):

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
        system_prompt: str | None = None,
    ):

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