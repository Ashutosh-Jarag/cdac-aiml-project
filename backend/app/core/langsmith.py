"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file configures environment variables required for LangChain tracing and monitoring (LangSmith integration).
It maps application settings from the central `settings` module directly to process-level environment variables
so that LangChain automatically detects project configurations and API credentials.

Key environment variables set:
  - LANGCHAIN_API_KEY: Authentication key for LangChain / LangSmith services.
  - LANGCHAIN_PROJECT: Target project name under which traces and logs are grouped.
  - LANGCHAIN_TRACING_V2: Lowercase boolean flag ('true'/'false') enabling or disabling LangChain V2 tracing.
"""

import os

from app.core.config import settings

# Set LangChain environment variables from application configuration
os.environ["LANGCHAIN_API_KEY"] = settings.LANGCHAIN_API_KEY
os.environ["LANGCHAIN_PROJECT"] = settings.LANGCHAIN_PROJECT
os.environ["LANGCHAIN_TRACING_V2"] = str(
    settings.LANGCHAIN_TRACING_V2
).lower()