"""
Publication Service Module
---------------------------
This module defines the `PublicationService` class, which uses a pre-trained XGBoost 
classification model to evaluate whether an academic paper manuscript is likely to be published.

It constructs a tabular feature payload from user request attributes—such as combined title/abstract text,
primary category, author count, word counts, comment length, DOI presence, and revision version counts—
and performs inference to estimate the publication probability and status.

Exports:
  - publication_service: Singleton instance of `PublicationService` for manuscript publication prediction.
"""

from pathlib import Path
from typing import Any

import joblib
import pandas as pd

# Directory path containing the publication prediction model artifact
MODEL_DIR = (
    Path(__file__).parent
    / "models"
    / "publication"
)

# Load trained XGBoost binary classification model
MODEL = joblib.load(
    MODEL_DIR / "publication_prediction_xgboost.pkl"
)


class PublicationService:
    """
    Service responsible for predicting the likelihood of manuscript publication 
    using an XGBoost classification model.
    """

    def predict(self, request: Any) -> dict[str, Any]:
        """
        Extracts features from an incoming publication request object, builds a Pandas DataFrame,
        and computes the prediction status and probability.

        Args:
            request (Any): Input request object containing manuscript attributes:
                           - title (str)
                           - abstract (str)
                           - category (str)
                           - author_count (int)
                           - comment_length (int)
                           - doi_exists (bool | int)
                           - version_count (int)

        Returns:
            dict[str, Any]: A dictionary containing:
                - "published" (bool): True if model predicts publication, False otherwise.
                - "probability" (float): Model confidence percentage rounded to 2 decimal places.
                - "status" (str): Human-readable prediction label.
        """

        sample = pd.DataFrame({
            "text": [
                request.title + " " + request.abstract
            ],
            "primary_category": [
                request.category
            ],
            "author_count": [
                request.author_count
            ],
            "title_word_count": [
                len(request.title.split())
            ],
            "abstract_word_count": [
                len(request.abstract.split())
            ],
            "comment_length": [
                request.comment_length
            ],
            "doi_exists": [
                int(request.doi_exists)
            ],
            "version_count": [
                request.version_count
            ]
        })

        prediction = int(
            MODEL.predict(sample)[0]
        )

        probability = float(
            MODEL.predict_proba(sample)[0][1]
        )

        return {
            "published": bool(prediction),
            "probability": round(probability * 100, 2),
            "status": (
                "Likely to be Published"
                if prediction
                else "Low Publication Probability"
            )
        }


# Global singleton instance
publication_service = PublicationService()