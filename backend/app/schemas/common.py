from enum import Enum

from pydantic import BaseModel


class InputQuality(str, Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    EXCELLENT = "Excellent"


class APIResponse(BaseModel):
    success: bool
    message: str