from pathlib import Path

# ==========================
# Project Paths
# ==========================

PROJECT_ROOT = Path(__file__).resolve().parent.parent

DATA_DIR = PROJECT_ROOT / "data"

RAW_DATA_DIR = DATA_DIR / "raw"
PROCESSED_DATA_DIR = DATA_DIR / "processed"
EMBEDDINGS_DIR = DATA_DIR / "embeddings"

MODEL_DIR = PROJECT_ROOT / "models"

LOG_DIR = PROJECT_ROOT / "logs"

DOCS_DIR = PROJECT_ROOT / "docs"

# Dataset

RAW_DATA_PATH = RAW_DATA_DIR / "arxiv-metadata-oai-snapshot.json"

# Sample size during development
SAMPLE_SIZE = 1000