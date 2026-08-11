"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data schemas and enumeration types for text summarization operations.
It provides validation models for summary requests and responses, allowing callers to specify
formatting styles (bulleted, short narrative, or detailed).

Classes & Enums:
  - SummaryStyle: String-based Enum defining supported summary output formatting options (BULLET, SHORT, DETAILED).
  - SummaryRequest: Input schema containing the source text to summarize and the desired SummaryStyle.
  - SummaryResponse: Output schema containing the generated summary string result.
"""

from enum import Enum

from pydantic import BaseModel


class SummaryStyle(str, Enum):
    """
    Enumeration of available formatting styles for generated summaries.

    Attributes:
        BULLET (str): Generates a bulleted list of key points ("bullet").
        SHORT (str): Generates a concise narrative overview ("short").
        DETAILED (str): Generates a comprehensive and in-depth summary ("detailed").
    """
    BULLET = "bullet"
    SHORT = "short"
    DETAILED = "detailed"


class SummaryRequest(BaseModel):
    """
    Schema for incoming text summarization request payloads.

    Attributes:
        text (str): The raw input body of text to be summarized.
        style (SummaryStyle): The desired formatting style for the output summary. Defaults to SummaryStyle.BULLET.
    """
    text: str

    style: SummaryStyle = SummaryStyle.BULLET


class SummaryResponse(BaseModel):
    """
    Schema for outgoing text summarization response payloads.

    Attributes:
        summary (str): The generated summary text string formatted according to the requested style.
    """
    summary: str