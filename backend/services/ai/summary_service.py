class SummaryService:

    def summarize(
        self,
        session_id: str,
        mode: str
    ):

        return {
            "summary": "Dummy summary.",
            "bullet_points": [
                "Point 1",
                "Point 2",
                "Point 3"
            ]
        }


summary_service = SummaryService()