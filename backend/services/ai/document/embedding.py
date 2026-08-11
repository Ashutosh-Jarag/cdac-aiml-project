"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `EmbeddingService` class, responsible for generating vector embeddings for text documents and search queries.
It wraps the `SentenceTransformer` framework using the `all-MiniLM-L6-v2` lightweight embedding model to convert raw text strings 
into standard Python list representations of vector floating-point numbers.

Key functionality:
  - __init__(): Loads the `all-MiniLM-L6-v2` SentenceTransformer model into memory during service initialization.
  - embed_documents(): Encodes a batch of document text strings into vector embedding lists for indexing.
  - embed_query(): Encodes a single user query string into a vector embedding list for similarity search.

Exports:
  - embedding_service: Singleton instance of `EmbeddingService` for application-wide vector embedding generation.
"""

from sentence_transformers import SentenceTransformer


class EmbeddingService:
    """
    Service class providing text embedding generation capabilities using SentenceTransformers.
    """

    def __init__(self):
        """
        Initializes the embedding service by loading the 'all-MiniLM-L6-v2' SentenceTransformer model.

        Args:
            None

        Returns:
            None
        """
        self.model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    def embed_documents(self, texts: list[str]) -> list[list[float]]:
        """
        Generates vector embeddings for a list of document text chunks.

        Args:
            texts (list[str]): List of text strings to be vectorized.

        Returns:
            list[list[float]]: List of vector embeddings represented as lists of float values.
        """
        return self.model.encode(
            texts,
            convert_to_numpy=True
        ).tolist()

    def embed_query(self, text: str) -> list[float]:
        """
        Generates a single vector embedding for an incoming user search query string.

        Args:
            text (str): The search query text string to be vectorized.

        Returns:
            list[float]: Vector embedding represented as a list of float values.
        """
        return self.model.encode(
            text,
            convert_to_numpy=True
        ).tolist()


# Global singleton instance of EmbeddingService
embedding_service = EmbeddingService()