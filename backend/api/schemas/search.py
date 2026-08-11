"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for vector or keyword search queries across research papers.
It structures request parameters and response data contracts for retrieving relevant scientific paper matches.

Classes:
  - SearchRequest: Input schema for specifying a search query string and specifying a top_k limit for results.
  - PaperResponse: Data schema representing detailed metadata for a matched paper (ID, title, authors, category, abstract, similarity score, URL).
  - SearchData: Response container schema encapsulating a list of matched PaperResponse items.
"""

from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    """
    Schema for incoming search request payloads.

    Attributes:
        query (str): The search query string (must be at least 2 characters long).
        top_k (int): Maximum number of top matching papers to return (constrained between 1 and 20). Defaults to 5.
    """
    query: str = Field(
        ...,
        min_length=2,
        description="Search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of papers"
    )


class PaperResponse(BaseModel):
    """
    Schema representing a single matched paper in search results.

    Attributes:
        id (str): Unique database or catalog identifier of the paper.
        title (str): Title of the paper.
        authors (list[str]): List of author names attributed to the paper.
        category (str): Primary subject category or topic classification.
        abstract (str): Abstract summary of the paper content.
        similarity (float): Similarity or relevance score computed for the query match.
        paper_url (str): Direct URL link to access the full paper document.
    """
    id: str

    title: str

    authors: list[str]

    category: str

    abstract: str

    similarity: float

    paper_url: str


class SearchData(BaseModel):
    """
    Schema wrapping the collection of search result paper items.

    Attributes:
        papers (list[PaperResponse]): List of matching paper metadata objects returned by the search service.
    """
    papers: list[PaperResponse]