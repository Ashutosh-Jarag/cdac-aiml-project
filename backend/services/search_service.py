from api.schemas.search import SearchData


class SearchService:

    def search(
        self,
        query: str,
        top_k: int
    ) -> SearchData:

        papers = [
            {
                "id": "001",
                "title": "Attention Is All You Need",
                "authors": [
                    "Ashish Vaswani",
                    "Noam Shazeer"
                ],
                "category": "cs.AI",
                "abstract": "Transformer architecture paper...",
                "similarity": 0.98,
                "paper_url": "https://arxiv.org/abs/1706.03762"
            }
        ]

        return SearchData(
            papers=papers
        )


search_service = SearchService()