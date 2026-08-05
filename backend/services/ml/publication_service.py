class PublicationService:

    def predict(
        self,
        request
    ):

        return {
            "published": True,
            "probability": 0.86
        }


publication_service = PublicationService()