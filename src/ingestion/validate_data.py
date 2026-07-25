import pandas as pd

from src.utils.logger import logger


class DataValidator:

    REQUIRED_COLUMNS = [
        "id",
        "title",
        "abstract",
        "authors",
        "categories"
    ]

    def validate(self, df: pd.DataFrame):

        logger.info("Starting Dataset Validation")

        # Check columns
        missing_cols = [
            col for col in self.REQUIRED_COLUMNS
            if col not in df.columns
        ]

        if missing_cols:
            raise ValueError(f"Missing Columns : {missing_cols}")

        # Duplicate IDs
        duplicates = df["id"].duplicated().sum()

        print(f"Duplicate IDs : {duplicates}")

        # Missing Values

        print(df[self.REQUIRED_COLUMNS].isnull().sum())

        logger.info("Validation Completed")