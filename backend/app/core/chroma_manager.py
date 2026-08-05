import chromadb
from chromadb.config import Settings


class ChromaManager:

    def __init__(self):

        self.client = chromadb.PersistentClient(
            path="./chroma_db",
            settings=Settings(
                anonymized_telemetry=False
            )
        )

    def get_collection(self, collection_name: str):

        return self.client.get_or_create_collection(
            name=collection_name
        )

    def delete_collection(self, collection_name: str):

        try:
            self.client.delete_collection(collection_name)
        except Exception:
            pass


chroma_manager = ChromaManager()