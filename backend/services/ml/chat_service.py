class MLChatService:

    def chat(
        self,
        question: str,
        provider: str | None,
        api_key: str | None
    ):

        return {
            "answer": "This is a dummy response from the Research Dataset.",
            "references": [
                {
                    "title": "Attention Is All You Need",
                    "paper_url": "https://arxiv.org/abs/1706.03762"
                }
            ]
        }


ml_chat_service = MLChatService()