"""
Recommendation Service Module
------------------------------
This module defines the `RecommendationService` class, which interacts with the 
recommendation model to retrieve and format paper recommendations based on title and abstract text.

Key functionality:
  - Invokes recommendation engine (`recommend` function) with specified parameters.
  - Formats recommendations with normalized similarity scores (scaled to percentages).
  - Handles missing metadata fields gracefully with default fallbacks.

Exports:
  - recommendation_service: Singleton instance of `RecommendationService` for recommendation requests.
"""

from typing import Any

from services.ml.models.recommendation.recommendation import (
    recommend
)


class RecommendationService:
    """
    Service responsible for querying the recommendation model and formatting
    paper recommendation payloads.
    """

    def recommend(
        self,
        title: str,
        abstract: str,
        top_k: int,
    ) -> dict[str, list[dict[str, Any]]]:
        """
        Retrieves top-k recommended research papers and converts similarity scores to percentages.

        Args:
            title (str): Paper title query.
            abstract (str): Paper abstract query text.
            top_k (int): Number of top recommendations to retrieve.

        Returns:
            dict[str, list[dict[str, Any]]]: Dictionary containing a list of recommended paper objects:
                - "id" (str): Paper identifier.
                - "title" (str): Paper title.
                - "authors" (str): Authors list.
                - "category" (str): Primary paper category code.
                - "similarity" (float): Relevance similarity percentage (rounded to 2 decimal places).
                - "update_date" (str): Paper publication or update date string.
        """

        recommendations = recommend(
            title=title,
            abstract=abstract,
            top_k=top_k,
        )

        papers = []

        for paper in recommendations:
            score = paper.get("score", 0)

            papers.append(
                {
                    "id": paper.get("id", ""),
                    "title": paper.get("title", ""),
                    "authors": paper.get("authors", ""),
                    "category": paper.get("category", ""),
                    "similarity": round(score * 100, 2),
                    "update_date": paper.get(
                        "update_date",
                        ""
                    ),
                }
            )

        return {
            "papers": papers
        }


# Global singleton instance
recommendation_service = RecommendationService()