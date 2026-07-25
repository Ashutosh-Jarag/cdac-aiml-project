from pathlib import Path

from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# ======================================================
# Project Paths
# ======================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DB_PATH = PROJECT_ROOT / "data" / "embeddings"

# ======================================================
# Embedding Model
# ======================================================

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

# ======================================================
# Vector Store
# ======================================================

vectorstore = Chroma(
    persist_directory=str(DB_PATH),
    embedding_function=embedding_model
)

# ======================================================
# Retriever
# ======================================================

retriever = vectorstore.as_retriever(
    search_type="similarity",
    search_kwargs={"k": 5}
)