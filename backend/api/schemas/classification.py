from pydantic import BaseModel

from app.schemas.common import InputQuality


class ClassificationRequest(BaseModel):
    title: str
    abstract: str | None = None


class ClassificationResponse(BaseModel):
    predicted_category: str
    confidence: float
    input_quality: InputQuality
    warning: str | None = None