"""
Prepare Publication Prediction Dataset

Reads the raw arXiv metadata dataset in chunks,
performs feature engineering,
and saves the processed data as a Parquet file.

Author: Ashutosh Jarag
"""

import os
import logging

import pandas as pd
from tqdm import tqdm
import pyarrow as pa
import pyarrow.parquet as pq

# =====================================================
# Configuration
# =====================================================

RAW_DATA = "data/raw/arxiv-metadata-oai-snapshot.json"

OUTPUT_DIR = "data/processed"

OUTPUT_FILE = os.path.join(
    OUTPUT_DIR,
    "publication_dataset.parquet"
)

CHUNK_SIZE = 100000


# =====================================================
# Logging
# =====================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


# =====================================================
# Required Columns
# =====================================================

COLUMNS = [
    "id",
    "title",
    "abstract",
    "authors",
    "categories",
    "comments",
    "journal-ref",
    "doi",
    "versions",
    "update_date"
]


# =====================================================
# Feature Engineering
# =====================================================

def transform_chunk(chunk: pd.DataFrame) -> pd.DataFrame:

    # Keep only required columns
    chunk = chunk[COLUMNS].copy()

    # Rename
    chunk.rename(
        columns={
            "journal-ref": "journal_ref"
        },
        inplace=True
    )

    # =================================================
    # Target Variable
    # =================================================

    chunk["published"] = (
        chunk["journal_ref"]
        .notna()
        .astype(int)
    )

    # =================================================
    # Text Features
    # =================================================

    chunk["title_char_count"] = (
        chunk["title"]
        .fillna("")
        .str.len()
    )

    chunk["abstract_char_count"] = (
        chunk["abstract"]
        .fillna("")
        .str.len()
    )

    chunk["title_word_count"] = (
        chunk["title"]
        .fillna("")
        .str.split()
        .str.len()
    )

    chunk["abstract_word_count"] = (
        chunk["abstract"]
        .fillna("")
        .str.split()
        .str.len()
    )

    # =================================================
    # Metadata Features
    # =================================================

    chunk["author_count"] = (
        chunk["authors"]
        .fillna("")
        .str.split(",")
        .str.len()
    )

    chunk["comment_length"] = (
        chunk["comments"]
        .fillna("")
        .str.len()
    )

    chunk["doi_exists"] = (
        chunk["doi"]
        .notna()
        .astype(int)
    )

    chunk["version_count"] = (
        chunk["versions"]
        .apply(lambda x: len(x) if isinstance(x, list) else 0)
    )

    # =================================================
    # Force Consistent Data Types
    # =================================================

    string_columns = [
        "id",
        "title",
        "abstract",
        "authors",
        "categories",
        "update_date"
    ]

    for col in string_columns:
        chunk[col] = (
            chunk[col]
            .fillna("")
            .astype(str)
        )

    # =================================================
    # Drop Unnecessary Columns
    # =================================================

    chunk.drop(
        columns=[
            "comments",
            "doi",
            "journal_ref",
            "versions"
        ],
        inplace=True
    )

    return chunk


# =====================================================
# Main ETL Pipeline
# =====================================================

def build_dataset():

    os.makedirs(
        OUTPUT_DIR,
        exist_ok=True
    )

    # Delete existing parquet file
    if os.path.exists(OUTPUT_FILE):
        os.remove(OUTPUT_FILE)
        logger.info("Old Parquet file removed.")

    reader = pd.read_json(
        RAW_DATA,
        lines=True,
        chunksize=CHUNK_SIZE
    )

    writer = None
    total_rows = 0

    logger.info("Starting dataset preparation...")

    for chunk_number, chunk in enumerate(tqdm(reader), start=1):

        chunk = transform_chunk(chunk)

        table = pa.Table.from_pandas(
            chunk,
            preserve_index=False
        )

        if writer is None:

            writer = pq.ParquetWriter(
                OUTPUT_FILE,
                table.schema
            )

        writer.write_table(table)

        total_rows += len(chunk)

        logger.info(
            f"Chunk {chunk_number} processed | Rows: {len(chunk):,}"
        )

    if writer is not None:
        writer.close()

    logger.info("=" * 60)
    logger.info("Dataset Created Successfully")
    logger.info(f"Output File : {OUTPUT_FILE}")
    logger.info(f"Total Rows  : {total_rows:,}")
    logger.info("=" * 60)


# =====================================================
# Entry Point
# =====================================================

if __name__ == "__main__":
    build_dataset()