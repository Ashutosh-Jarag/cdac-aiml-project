from pydantic import BaseModel, Field


class RecommendationRequest(BaseModel):

    title: str

    abstract: str | None = None

    top_k: int = Field(
        default=5,
        ge=1,
        le=20
    )


class RecommendedPaper(BaseModel):

    title: str

    authors: str

    category: str

    distance: float


class RecommendationResponse(BaseModel):

    papers: list[RecommendedPaper]