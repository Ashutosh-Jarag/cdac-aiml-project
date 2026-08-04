from app.core.logger import logger


class ModelLoader:

    def __init__(self):
        self.models = {}

    def load_models(self):
        logger.info("Loading ML models...")

        # TODO:
        # self.models["classification"] = joblib.load(...)
        # self.models["publication"] = joblib.load(...)

        logger.success("Models loaded.")

    def get(self, name):
        return self.models.get(name)


model_loader = ModelLoader()