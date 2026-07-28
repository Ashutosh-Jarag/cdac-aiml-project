import gc
import logging
from pathlib import Path

import joblib
import pandas as pd

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC

from sklearn.metrics import (
    accuracy_score,
    classification_report,
    f1_score,
)

# -----------------------------------------------------
# Configuration
# -----------------------------------------------------

DATA_PATH = Path("data/processed/publication_dataset.parquet")

MODEL_DIR = Path("models/classification")

MODEL_DIR.mkdir(parents=True, exist_ok=True)

CATEGORY_THRESHOLD = 1000

SAMPLE_SIZE = 300000

RANDOM_STATE = 42

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)

# -----------------------------------------------------
# Load Dataset
# -----------------------------------------------------

logging.info("Loading Dataset...")

df = pd.read_parquet(
    DATA_PATH,
    columns=[
        "title",
        "abstract",
        "categories"
    ]
)

logging.info(f"Dataset Shape : {df.shape}")

# -----------------------------------------------------
# Create Features
# -----------------------------------------------------

logging.info("Preparing Text...")

df["text"] = (
    df["title"].fillna("")
    + " "
    + df["abstract"].fillna("")
)

df["primary_category"] = (
    df["categories"]
    .fillna("Unknown")
    .str.split()
    .str[0]
)

# -----------------------------------------------------
# Remove Rare Categories
# -----------------------------------------------------

logging.info("Filtering Categories...")

category_counts = df["primary_category"].value_counts()

valid_categories = category_counts[
    category_counts >= CATEGORY_THRESHOLD
].index

df = df[
    df["primary_category"].isin(valid_categories)
]

logging.info(f"Remaining Rows : {len(df):,}")

logging.info(f"Remaining Categories : {df['primary_category'].nunique()}")

# -----------------------------------------------------
# Sample
# -----------------------------------------------------

logging.info(f"Sampling {SAMPLE_SIZE:,} papers...")

sample_df = (
    df.sample(
        n=SAMPLE_SIZE,
        random_state=RANDOM_STATE
    )
    .reset_index(drop=True)
)

del df

gc.collect()

logging.info(sample_df.shape)

# -----------------------------------------------------
# Label Encoding
# -----------------------------------------------------

encoder = LabelEncoder()

y = encoder.fit_transform(
    sample_df["primary_category"]
)

X = sample_df["text"]

del sample_df

gc.collect()

# -----------------------------------------------------
# Train Test Split
# -----------------------------------------------------

logging.info("Splitting Dataset...")

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=RANDOM_STATE,
    stratify=y
)

# -----------------------------------------------------
# Pipeline
# -----------------------------------------------------

logging.info("Building Pipeline...")

pipeline = Pipeline([

    (
        "tfidf",
        TfidfVectorizer(
            lowercase=True,
            stop_words="english",
            max_features=30000,
            ngram_range=(1, 2),
            min_df=2,
            max_df=0.95,
        ),
    ),

    (
        "svm",
        LinearSVC(
            class_weight="balanced",
            random_state=RANDOM_STATE,
        ),
    ),
])

# -----------------------------------------------------
# Train
# -----------------------------------------------------

logging.info("Training SVM...")

pipeline.fit(
    X_train,
    y_train,
)

# -----------------------------------------------------
# Evaluate
# -----------------------------------------------------

logging.info("Evaluating...")

pred = pipeline.predict(
    X_test
)

print("=" * 70)

print(
    "Accuracy :",
    accuracy_score(
        y_test,
        pred,
    ),
)

print(
    "Macro F1 :",
    f1_score(
        y_test,
        pred,
        average="macro",
    ),
)

print("=" * 70)

print(
    classification_report(
        y_test,
        pred,
        target_names=encoder.classes_,
        zero_division=0,
    )
)

# -----------------------------------------------------
# Save
# -----------------------------------------------------

logging.info("Saving Models...")

joblib.dump(
    pipeline,
    MODEL_DIR / "svm_pipeline.pkl",
)

joblib.dump(
    encoder,
    MODEL_DIR / "label_encoder.pkl",
)

logging.info("Done.")