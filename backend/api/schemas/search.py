from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(
        ...,
        min_length=2,
        description="Search query"
    )

    top_k: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Maximum number of papers"
    )


class PaperResponse(BaseModel):

    id: str

    title: str

    authors: list[str]

    category: str

    abstract: str

    similarity: float

    paper_url: str


class SearchData(BaseModel):

    papers: list[PaperResponse]