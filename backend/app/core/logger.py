"""
FILE CONTENTS & OVERVIEW:
-------------------------
This file configures application-wide structured logging using the Loguru library.
It sets up log formatting, output destinations (console and rolling log file), severity filtering,
and log rotation/retention policies.

Key configurations:
  - Console Sink (sys.stdout): Formatted colored output filtering at INFO level and above.
  - File Sink ("logs/researchai.log"): Persistent log file with a 10 MB rotation limit, 
    10-day retention policy, and INFO level filtering.

Exports:
  - logger: Re-exported configured Loguru logger instance for application-wide logging.
"""

import sys
from loguru import logger

# Remove default Loguru handler to prevent duplicate log outputs
logger.remove()

# Configure standard stdout console logging sink with custom formatting
logger.add(
    sys.stdout,
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
           "<level>{level}</level> | "
           "{message}",
)

# Configure file logging sink with rotation and retention rules
logger.add(
    "logs/researchai.log",
    rotation="10 MB",
    retention="10 days",
    level="INFO",
)

# Specify public interface exports
__all__ = ["logger"]