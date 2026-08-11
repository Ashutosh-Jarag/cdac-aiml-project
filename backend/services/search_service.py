"""
Search Service Module
---------------------
This module defines the `SearchService` class, which handles academic paper search queries.
It executes search queries against vector indexes or database repositories and returns structured 
Pydantic model instances (`SearchData`).

Key functionality:
  - search(): Processes search query strings and returns matching research papers along with similarity scores and URLs. 
              Currently returns structured mock/stub data.

Exports:
  - search_service: Singleton instance of `SearchService` for application-wide academic paper searches.
"""

from api.schemas.search import SearchData


class SearchService:
    """
    Service class responsible for searching research paper databases and returning structured results.
    """

    def search(
        self,
        query: str,
        top_k: int,
    ) -> SearchData:
        """
        Executes a search query for research papers and returns matching results.

        Args:
            query (str): Search text query string.
            top_k (int): Maximum number of top relevant papers to return.

        Returns:
            SearchData: Pydantic model instance containing the list of matching paper objects.
        """

        papers = [
            {
                "id": "001",
                "title": "Attention Is All You Need",
                "authors": [
                    "Ashish Vaswani",
                    "Noam Shazeer",
                ],
                "category": "cs.AI",
                "abstract": "Transformer architecture paper...",
                "similarity": 0.98,
                "paper_url": "https://arxiv.org/abs/1706.03762",
            }
        ]

        return SearchData(
            papers=papers
        )


# Global singleton instance of SearchService
search_service = SearchService()