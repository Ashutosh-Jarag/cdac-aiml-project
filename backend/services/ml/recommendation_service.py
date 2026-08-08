from services.ml.models.recommendation.recommendation import (
    recommend
)


class RecommendationService:

    def recommend(
        self,
        title: str,
        abstract: str,
        top_k: int
    ):

        recommendations = recommend(
            title=title,
            abstract=abstract,
            top_k=top_k
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
                    )
                }
            )

        return {
            "papers": papers
        }


recommendation_service = RecommendationService()