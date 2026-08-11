"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for Machine Learning (ML) services.
It covers request and response data contracts across four main ML functional domains:
  1. Classification: Schemas for categorizing research papers by title and abstract into code/name categories.
  2. Publication Prediction: Schemas for predicting whether a paper will be published based on metadata metrics.
  3. Recommendation: Schemas for finding similar research papers based on semantic text input and top-k limits.
  4. ML Chat: Schemas for AI-driven Q&A tasks with source paper citations.
"""

from pydantic import BaseModel, Field


# ---------- Classification ----------

class ClassificationRequest(BaseModel):
    """
    Schema for paper classification request payloads.

    Attributes:
        title (str): Title of the research paper (minimum length of 3 characters).
        abstract (str): Abstract of the research paper (minimum length of 10 characters).
    """
    title: str = Field(..., min_length=3)
    abstract: str = Field(..., min_length=10)


class Category(BaseModel):
    """
    Schema representing a single classified topic category.

    Attributes:
        code (str): Short classification code or taxonomy identifier (e.g., 'cs.AI').
        name (str): Full human-readable name of the category.
    """
    code: str
    name: str


class ClassificationResponse(BaseModel):
    """
    Schema for classification prediction responses.

    Attributes:
        categories (list[Category]): List of predicted categories assigned to the paper.
    """
    categories: list[Category]


# ---------- Publication Prediction ----------

class PublicationRequest(BaseModel):
    """
    Schema for publication probability prediction requests.

    Attributes:
        title (str): Title of the paper.
        abstract (str): Abstract content of the paper.
        category (str): Primary subject category of the paper.
        author_count (int): Total number of contributing authors.
        comment_length (int): Character length of accompanying comments or notes.
        doi_exists (bool): Flag indicating whether a Digital Object Identifier (DOI) exists.
        version_count (int): Total number of submitted revision versions.
    """
    title: str
    abstract: str
    category: str
    author_count: int
    comment_length: int
    doi_exists: bool
    version_count: int


class PublicationResponse(BaseModel):
    """
    Schema for publication probability prediction responses.

    Attributes:
        published (bool): Binary prediction outcome indicating if publication is likely.
        probability (float): Model confidence score/probability of publication (0.0 to 1.0).
    """
    published: bool
    probability: float


# ---------- Recommendation ----------

class RecommendationRequest(BaseModel):
    """
    Schema for requesting paper recommendations.

    Attributes:
        title (str): Reference paper title.
        abstract (str): Reference paper abstract.
        top_k (int): Number of recommended papers to return (constrained between 1 and 20, default: 5).
    """
    title: str
    abstract: str
    top_k: int = Field(default=5, ge=1, le=20)


class RecommendedPaper(BaseModel):
    """
    Schema representing a single recommended research paper item.

    Attributes:
        title (str): Title of the recommended paper.
        authors (str): Author attribution string for the paper.
        category (str): Subject category of the paper.
        similarity (float): Similarity score relative to the query paper.
        paper_url (str): Direct URL link to the paper.
    """
    title: str
    authors: str
    category: str
    similarity: float
    paper_url: str


class RecommendationResponse(BaseModel):
    """
    Schema for paper recommendation responses.

    Attributes:
        papers (list[RecommendedPaper]): List of top-k recommended paper objects.
    """
    papers: list[RecommendedPaper]


# ---------- ML Chat ----------

class MLChatRequest(BaseModel):
    """
    Schema for machine learning chat query requests.

    Attributes:
        question (str): The user's query or prompt string.
        provider (str | None): Optional specified LLM service provider. Defaults to None.
        api_key (str | None): Optional API key override for the LLM provider. Defaults to None.
    """
    question: str
    provider: str | None = None
    api_key: str | None = None


class SourcePaper(BaseModel):
    """
    Schema representing a cited source paper supporting the chat answer.

    Attributes:
        title (str): Title of the referenced paper.
        paper_url (str): Web link to access the referenced source paper.
    """
    title: str
    paper_url: str


class MLChatResponse(BaseModel):
    """
    Schema for machine learning chat query responses.

    Attributes:
        answer (str): The generated response text.
        references (list[SourcePaper]): List of cited source papers supporting the answer.
    """
    answer: str
    references: list[SourcePaper]