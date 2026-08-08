from pydantic import BaseModel, Field

from app.schemas.common import InputQuality


class PublicationPredictionRequest(BaseModel):

    title: str

    abstract: str | None = None

    category: str | None = None

    authors: str | None = None

    comments: str | None = None

    doi_exists: bool = False

    version_count: int = Field(
        default=1,
        ge=1,
        le=20
    )


class PublicationPredictionResponse(BaseModel):

    prediction: str

    probability: float = Field(
        ge=0,
        le=100
    )

    input_quality: InputQuality

    warning: str | None = None