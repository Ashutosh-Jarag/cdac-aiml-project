from pathlib import Path

import joblib
import pandas as pd


MODEL_DIR = (
    Path(__file__).parent
    / "models"
    / "publication"
)

MODEL = joblib.load(
    MODEL_DIR / "publication_prediction_xgboost.pkl"
)


class PublicationService:

    def predict(self, request):

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

publication_service = PublicationService()