"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for machine learning classification operations.
It structures request inputs and response outputs when evaluating academic titles and abstracts for category prediction.

Classes:
  - ClassificationRequest: Input schema containing title and optional abstract fields.
  - ClassificationResponse: Output schema containing category predictions, confidence scores, 
    input quality evaluations, and optional warning messages.
"""

from pydantic import BaseModel

from app.schemas.common import InputQuality


class ClassificationRequest(BaseModel):
    """
    Schema for incoming classification request payloads.

    Attributes:
        title (str): Title text of the paper/document to be classified.
        abstract (str | None): Optional abstract text providing additional context. Defaults to None.
    """
    title: str
    abstract: str | None = None


class ClassificationResponse(BaseModel):
    """
    Schema for outgoing classification result payloads.

    Attributes:
        predicted_category (str): The predicted classification label or category name.
        confidence (float): Model prediction confidence score (typically between 0.0 and 1.0).
        input_quality (InputQuality): Quality evaluation metric/enum for the provided input data.
        warning (str | None): Optional warning message regarding low confidence, short inputs, or quality flags. Defaults to None.
    """
    predicted_category: str
    confidence: float
    input_quality: InputQuality
    warning: str | None = None