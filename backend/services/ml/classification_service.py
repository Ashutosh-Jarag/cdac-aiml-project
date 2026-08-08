from pathlib import Path
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

    def predict(
        self,
        title: str,
        abstract: str,
    ):

        text = preprocess_text(
            title + " " + abstract
        )

        vector = tfidf.transform([text])

        prediction = MODEL.predict(vector)

        categories = mlb.inverse_transform(
            prediction
        )[0]

        result = []
        for code in categories:
            result.append({
                "code": code,
                "name": CATEGORY_MAP.get(code, code)
            })

        return {
            "categories": result
        }


classification_service = ClassificationService()