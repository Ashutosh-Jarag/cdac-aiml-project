class RecommendationService:

    def recommend(
        self,
        query: str,
        top_k: int
    ):

        return {
            "papers": [
                {
                    "title": "Attention Is All You Need",
                    "similarity": 0.98,
                    "category": "cs.AI",
                    "paper_url": "https://arxiv.org/abs/1706.03762"
                }
            ]
        }


recommendation_service = RecommendationService()