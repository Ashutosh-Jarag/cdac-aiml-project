"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `VectorStore` wrapper class, providing high-level operations for storing and querying
vector embeddings within ChromaDB collections using the central `chroma_manager`.

Key functionality:
  - add_documents(): Adds text chunks, vector embeddings, unique document IDs, and metadata to a specified ChromaDB collection.
  - search(): Queries a specified ChromaDB collection using a query vector embedding and returns the top-k nearest matches.

Exports:
  - vector_store: Singleton instance of `VectorStore` for application-wide vector persistence and retrieval operations.
"""

from typing import Any
from app.core.chroma_manager import chroma_manager


class VectorStore:
    """
    Service class wrapping ChromaDB operations for indexing and retrieving vector-embedded document chunks.
    """

    def add_documents(
        self,
        collection_name: str,
        chunks: list[Any],
        embeddings: list[list[float]],
    ) -> None:
        """
        Stores document chunks and their corresponding vector embeddings in a ChromaDB collection.

        Args:
            collection_name (str): The name of the target ChromaDB collection.
            chunks (list[Any]): List of LangChain Document objects containing `page_content` and `metadata`.
            embeddings (list[list[float]]): List of pre-computed vector embeddings corresponding to each chunk.

        Returns:
            None
        """
        collection = chroma_manager.get_collection(
            collection_name
        )

        collection.add(
            ids=[
                str(i)
                for i in range(len(chunks))
            ],
            documents=[
                chunk.page_content
                for chunk in chunks
            ],
            embeddings=embeddings,
            metadatas=[
                chunk.metadata
                for chunk in chunks
            ]
        )

    def search(
        self,
        collection_name: str,
        query_embedding: list[float],
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Executes a similarity search against a ChromaDB collection using a query embedding.

        Args:
            collection_name (str): The name of the target ChromaDB collection to search against.
            query_embedding (list[float]): Vector embedding representation of the search query.
            top_k (int, optional): The maximum number of top matching results to retrieve. Defaults to 5.

        Returns:
            dict[str, Any]: Query results dictionary returned by ChromaDB containing matched documents, metadatas, and distances.
        """
        collection = chroma_manager.get_collection(
            collection_name
        )

        return collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )


# Global singleton instance of VectorStore
vector_store = VectorStore()