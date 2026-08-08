import os

from app.core.config import settings

os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
os.environ["LANGCHAIN_TRACING_V2"] = str(
    settings.LANGCHAIN_TRACING_V2
).lower()