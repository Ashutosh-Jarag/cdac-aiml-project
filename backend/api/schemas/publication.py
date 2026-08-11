"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for publication prediction services.
It structures request inputs and response outputs for estimating publication outcomes and probabilities
based on paper metadata such as title, abstract, categories, author list, comments, DOI presence, and revision counts.

Classes:
  - PublicationPredictionRequest: Input schema for paper metadata attributes with validation constraints.
  - PublicationPredictionResponse: Output schema containing prediction results, percentage probabilities,
    input quality evaluations, and optional warning messages.
"""

from pydantic import BaseModel, Field

from app.schemas.common import InputQuality


class PublicationPredictionRequest(BaseModel):
    """
    Schema for publication prediction request payloads.

    Attributes:
        title (str): Title of the research paper.
        abstract (str | None): Optional abstract content of the paper. Defaults to None.
        category (str | None): Optional primary subject category string. Defaults to None.
        authors (str | None): Optional formatted string listing paper authors. Defaults to None.
        comments (str | None): Optional additional comments or submission notes. Defaults to None.
        doi_exists (bool): Flag indicating whether a Digital Object Identifier (DOI) exists. Defaults to False.
        version_count (int): Total number of submitted paper versions (constrained between 1 and 20). Defaults to 1.
    """
    title: str
    abstract: str | None = None
    category: str | None = None
    authors: str | None = None
    comments: str | None = None
    doi_exists: bool = False
    version_count: int = Field(
        default=1,
        ge=1,
        le=20
    )


class PublicationPredictionResponse(BaseModel):
    """
    Schema for publication prediction response payloads.

    Attributes:
        prediction (str): Predicted publication status outcome (e.g., "Accepted", "Rejected", "Published").
        probability (float): Estimated likelihood percentage score (constrained between 0.0 and 100.0).
        input_quality (InputQuality): Quality assessment enum/metric derived from the provided request input data.
        warning (str | None): Optional notice or warning regarding missing fields or low confidence scores. Defaults to None.
    """
    prediction: str
    probability: float = Field(
        ge=0,
        le=100
    )
    input_quality: InputQuality
    warning: str | None = None