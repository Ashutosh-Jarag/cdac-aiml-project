"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the ChromaDB management service for handling vector database interactions.
It encapsulates persistent client initialization and provides operational utility methods to create,
retrieve, or delete collections within the local Chroma vector store (`./chroma_db`).

Classes & Objects:
  - ChromaManager: Wrapper class managing ChromaDB client setup and collection lifecycle operations.
  - chroma_manager: Pre-instantiated singleton instance of ChromaManager for application-wide use.
"""

import chromadb
from chromadb.config import Settings


class ChromaManager:
    """
    Manager class responsible for ChromaDB vector database connection and collection operations.
    """

    def __init__(self):
        """
        Initializes the ChromaManager instance with a persistent ChromaDB client stored at './chroma_db'.
        Disables anonymized telemetry via configuration settings.

        Args:
            None

        Returns:
            None
        """
        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False
            )
        )

    def get_collection(self, collection_name: str):
        """
        Retrieves an existing Chroma collection by name or creates a new one if it does not exist.

        Args:
            collection_name (str): The unique name of the vector collection to access or create.

        Returns:
            chromadb.api.models.Collection.Collection: The requested or created ChromaDB collection object.
        """
        return self.client.get_or_create_collection(
            name=collection_name
        )

    def delete_collection(self, collection_name: str):
        """
        Deletes a Chroma collection by name. Silently catches and passes exceptions if the collection does not exist.

        Args:
            collection_name (str): The unique name of the vector collection to delete.

        Returns:
            None
        """
        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass


# Global singleton instance of ChromaManager
chroma_manager = ChromaManager()