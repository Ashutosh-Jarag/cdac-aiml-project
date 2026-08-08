from pathlib import Path

import chromadb
from sentence_transformers import SentenceTransformer

# ==========================================================
# Project Paths
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

EMBEDDINGS_DB_PATH = PROJECT_ROOT / "data" / "embeddings"

# ==========================================================
# Embedding Model
# ==========================================================

embedding_model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)

# ==========================================================
# Chroma Client
# ==========================================================

client = chromadb.PersistentClient(
    path=str(EMBEDDINGS_DB_PATH)
)

collection = client.get_collection(
    "research_papers"
)

# ==========================================================
# Retrieval Function
# ==========================================================

def retrieve_papers(
    query: str,
    top_k: int = 5
) -> dict:
    """
    Retrieve Top-K most relevant papers from ChromaDB.
    """

    query_embedding = embedding_model.encode(
        query
    ).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    return results