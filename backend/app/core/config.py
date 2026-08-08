from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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
        env_file=".env",
        extra="ignore"
    )


settings = Settings()


from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
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


    LANGCHAIN_API_KEY: str = ""
    LANGCHAIN_PROJECT: str = "aiml-project"
    LANGCHAIN_TRACING_V2: bool = False

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )


settings = Settings()


