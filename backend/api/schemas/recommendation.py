"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for paper recommendation operations.
It structures request inputs and response outputs for identifying related research papers based on input text metadata and similarity/distance metrics.

Classes:
  - RecommendationRequest: Input schema for recommendation queries, including paper title, optional abstract, and top_k result limits.
  - RecommendedPaper: Schema representing an individual recommended paper with title, authors, category, and distance score.
  - RecommendationResponse: Output schema encapsulating a list of recommended paper objects.
"""

from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):
    """
    Schema for incoming paper recommendation request payloads.

    Attributes:
        title (str): Title of the reference paper used for matching.
        abstract (str | None): Optional abstract content providing additional context. Defaults to None.
        top_k (int): Maximum number of recommended papers to return (constrained between 1 and 20). Defaults to 5.
    """
    title: str
    abstract: str | None = None
    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )


class RecommendedPaper(BaseModel):
    """
    Schema representing a single recommended paper result.

    Attributes:
        title (str): Title of the recommended paper.
        authors (str): Author attribution string for the recommended paper.
        category (str): Subject category or domain classification of the paper.
        distance (float): Vector distance or dissimilarity score relative to the query paper.
    """
    title: str
    authors: str
    category: str
    distance: float


class RecommendationResponse(BaseModel):
    """
    Schema for outgoing paper recommendation response payloads.

    Attributes:
        papers (list[RecommendedPaper]): List of recommended paper items sorted by relevance.
    """
    papers: list[RecommendedPaper]