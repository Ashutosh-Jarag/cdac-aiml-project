class ClassificationService:

    def predict(
        self,
        title: str,
        abstract: str
    ):

        return {
            "category": "cs.AI",
            "confidence": 0.97
        }


classification_service = ClassificationService()