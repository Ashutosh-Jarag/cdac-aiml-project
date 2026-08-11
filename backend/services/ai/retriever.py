"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `Retriever` service class, responsible for performing semantic document retrieval
over stored vector representations in ChromaDB.

Key functionality:
  - retrieve(): Embeds incoming search query strings using `embedding_service`, searches the specified
    ChromaDB vector collection (`session_id`), and returns matched document contents along with metadata.
    Raises an `AppException` (404) if no matching documents are retrieved.

Exports:
  - retriever: Singleton instance of `Retriever` for application-wide similarity search operations.
"""

from typing import Any
from app.core.exceptions import AppException
from app.core.logger import logger

from services.ai.document.embedding import embedding_service
from services.ai.document.vector_store import vector_store


class Retriever:
    """
    Service class handling semantic search and document chunk retrieval from vector storage.
    """

    def retrieve(
        self,
        session_id: str,
        question: str,
        top_k: int = 5,
    ) -> dict[str, Any]:
        """
        Retrieves the top-k most relevant document chunks for a given question from ChromaDB.

        Args:
            session_id (str): Unique collection identifier (chat session ID) in vector storage.
            question (str): The search query text string.
            top_k (int, optional): Maximum number of document chunks to retrieve. Defaults to 5.

        Returns:
            dict[str, Any]: Search results dictionary containing matching document texts, metadatas, and distances.

        Raises:
            AppException: If no document chunks are found or matched for the session (404).
        """
        embedding = embedding_service.embed_query(question)

        results = vector_store.search(
            collection_name=session_id,
            query_embedding=embedding,
            top_k=top_k,
        )

        if not results["documents"] or not results["documents"][0]:
            raise AppException(
                "No relevant information found.",
                404,
            )

        logger.info(
            f"Retrieved {len(results['documents'][0])} chunk(s)"
        )

        return results


# Global singleton instance of Retriever
retriever = Retriever()