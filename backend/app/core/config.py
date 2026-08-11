"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file manages environment variable parsing and configuration settings for the application.
It utilizes Pydantic's `BaseSettings` and `SettingsConfigDict` to load configuration values 
from an environment file (`.env`) located at the project root directory.

Key configurations managed:
  - Base paths & project directory structure.
  - App metadata (name, version, debug status).
  - Server binding details (host, port).
  - AI provider & key settings (Gemini API key, default provider).
  - Storage & ML model file paths (ChromaDB, model path).
  - Logging & CORS origin parameters.
  - Database connection credentials (host, port, DB name, user, password).

Classes & Objects:
  - Settings: BaseSettings class mapping and validating environment variables.
  - settings: Global instantiated Settings object providing typed access to configuration properties.
"""

from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict


# Project root path computation based on location:
# aiml-project/
# ├── .env
# └── backend/
#     └── app/
#         └── core/
#             └── config.py
BASE_DIR = Path(__file__).resolve().parents[3]


class Settings(BaseSettings):
    """
    Application configuration settings validated through Pydantic BaseSettings.
    Automatically reads variables from the environment or a specified `.env` file.

    Attributes:
        APP_NAME (str): Name of the application.
        APP_VERSION (str): Application version string.
        DEBUG (bool): Debug mode flag (True/False).
        HOST (str): Server host address (e.g., "127.0.0.1" or "0.0.0.0").
        PORT (int): Port number on which the server runs.
        DEFAULT_AI_PROVIDER (str): Default AI model provider identifier.
        GEMINI_API_KEY (str): API key for Google Gemini services. Defaults to empty string.
        CHROMA_DB_PATH (str): Directory path for persistent ChromaDB storage.
        MODEL_PATH (str): File path for local machine learning model artifacts.
        LOG_LEVEL (str): Logging severity level (e.g., "INFO", "DEBUG", "ERROR").
        CORS_ORIGINS (str): Allowed Cross-Origin Resource Sharing (CORS) origins string.
        DB_HOST (str): Database server hostname or IP address.
        DB_PORT (int): Port number for database connection.
        DB_NAME (str): Target database name.
        DB_USER (str): Database access username.
        DB_PASSWORD (str): Database access password.
        model_config (SettingsConfigDict): Pydantic settings configuration specifying
                                            env_file path and ignoring extra key inputs.
    """
    APP_NAME: str
    APP_VERSION: str
    DEBUG: bool

    HOST: str
    PORT: int

    DEFAULT_AI_PROVIDER: str

    GEMINI_API_KEY: str = ""

    CHROMA_DB_PATH: str
    MODEL_PATH: str

    LOG_LEVEL: str
    CORS_ORIGINS: str

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        extra="ignore",
    )


# Instantiate global settings object for access across the application
settings = Settings()