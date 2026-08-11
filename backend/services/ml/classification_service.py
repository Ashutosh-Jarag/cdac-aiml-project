"""
Classification Service Module
------------------------------
This module defines the `ClassificationService` class, which performs multi-label text 
classification on academic research papers using TF-IDF vectorization and a Support Vector 
Machine (SVM) model. It maps predicted category codes (e.g., 'cs', 'physics') to human-readable 
domain titles based on the arXiv category taxonomy.

Key functionality:
  - Text normalization via custom preprocessing steps.
  - TF-IDF feature extraction (`tfidf_vectorizer`).
  - SVM prediction model (`model_svm.pkl`).
  - Multi-label binarizer inverse transformation (`mlb_labels`).
  - Mapping predictions to arXiv top-level subject domains.

Exports:
  - classification_service: Singleton instance of `ClassificationService` for document category inference.
"""

from pathlib import Path
from typing import Any
import joblib

from services.ml.preprocessing import preprocess_text

# Mapping category codes to full human-readable names
CATEGORY_MAP = {
    "cs": "Computer Science",
    "econ": "Economics",
    "eess": "Electrical Engineering and Systems Science",
    "math": "Mathematics",
    "physics": "Physics",
    "q-bio": "Quantitative Biology",
    "q-fin": "Quantitative Finance",
    "stat": "Statistics",
}

MODEL_DIR = (
    Path(__file__).parent
    / "models"
    / "category"
)

PREPROCESSING = joblib.load(
    MODEL_DIR / "preprocessing.pkl"
)

MODEL = joblib.load(
    MODEL_DIR / "model_svm.pkl"
)

tfidf = PREPROCESSING["tfidf_vectorizer"]

mlb = PREPROCESSING["mlb_labels"]


class ClassificationService:
    """
    Service responsible for classifying research paper titles and abstracts
    into arXiv subject categories using TF-IDF and linear SVM models.
    """

    def predict(
        self,
        title: str,
        abstract: str,
    ) -> dict[str, list[dict[str, str]]]:
        """
        Predicts category codes and full domain names for a given title and abstract.

        Args:
            title (str): Paper title.
            abstract (str): Paper abstract text.

        Returns:
            dict[str, list[dict[str, str]]]: A payload containing a list of dictionaries 
                                             with category code and display name.
        """

        text = preprocess_text(
            title + " " + abstract
        )

        vector = tfidf.transform([text])

        prediction = MODEL.predict(vector)

        categories = mlb.inverse_transform(
            prediction
        )[0]

        result = [
            {
                "code": code,
                "name": CATEGORY_MAP.get(code, code),
            }
            for code in categories
        ]

        return {
            "categories": result
        }


# Global singleton instance
classification_service = ClassificationService()