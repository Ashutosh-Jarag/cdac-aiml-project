import pandas as pd

from config.config import RAW_DATA_PATH
from src.utils.logger import logger


class DataLoader:

    def __init__(self, file_path=RAW_DATA_PATH):
        self.file_path = file_path

    def load_data(self, n_rows=None):

        logger.info(f"Loading dataset from {self.file_path}")

        df = pd.read_json(
            self.file_path,
            lines=True,
            nrows=n_rows
        )

        logger.info(f"Dataset Loaded : {df.shape}")

        return df


if __name__ == "__main__":

    loader = DataLoader()

    df = loader.load_data(1000)

    print(df.head())

    print(df.shape)