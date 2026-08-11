"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines Pydantic data validation schemas for simple chat interaction interfaces.
It structures request inputs and response outputs for conversational AI endpoints that cite academic or reference sources:
  1. ChatRequest: Input payload schema containing the user's question string.
  2. SourcePaper: Schema representing metadata (title, authors, category) for cited reference papers.
  3. ChatResponse: Output payload schema containing the generated answer and a list of source paper references.
"""

from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Schema for incoming chat request payloads.

    Attributes:
        question (str): The user's query or question string.
    """
    question: str


class SourcePaper(BaseModel):
    """
    Schema representing a cited source paper supporting the chat answer.

    Attributes:
        title (str): Title of the referenced paper.
        authors (str): Author attribution string for the paper.
        category (str): Subject category or domain of the referenced paper.
    """
    title: str
    authors: str
    category: str


class ChatResponse(BaseModel):
    """
    Schema for outgoing chat response payloads.

    Attributes:
        answer (str): The AI-generated answer text.
        sources (list[SourcePaper]): List of cited source papers supporting the answer.
    """
    answer: str
    sources: list[SourcePaper]