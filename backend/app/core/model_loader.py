"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file defines the `ModelLoader` class responsible for managing and lazily/eagerly loading
machine learning models (e.g., classification, publication models) into memory.
It acts as a central registry to load, store, and retrieve trained model artifacts across the application.

Classes & Objects:
  - ModelLoader: Singleton wrapper class to manage model loading and lifecycle access.
  - model_loader: Pre-instantiated global instance of ModelLoader for application-wide model access.
"""

from app.core.logger import logger


class ModelLoader:
    """
    Registry and manager class for loading and retrieving trained Machine Learning models.

    Attributes:
        models (dict): In-memory dictionary mapping model names to loaded model instances or artifacts.
    """

    def __init__(self):
        """
        Initializes an empty ModelLoader instance with a models dictionary.

        Args:
            None

        Returns:
            None
        """
        self.models = {}

    def load_models(self):
        """
        Loads ML models into memory and populates the models dictionary.
        Logs startup progress and completion events.

        Args:
            None

        Returns:
            None
        """
        logger.info("Loading ML models...")

        # TODO: Implement model loading logic
        # Example:
        # self.models["classification"] = joblib.load(settings.MODEL_PATH / "classification.joblib")
        # self.models["publication"] = joblib.load(settings.MODEL_PATH / "publication.joblib")

        logger.success("Models loaded.")

    def get(self, name: str):
        """
        Retrieves a loaded ML model by name from the models registry dictionary.

        Args:
            name (str): The identifier key of the requested model (e.g., 'classification', 'publication').

        Returns:
            Any | None: The loaded ML model instance if present, or None if not found.
        """
        return self.models.get(name)


# Global singleton instance of ModelLoader
model_loader = ModelLoader()