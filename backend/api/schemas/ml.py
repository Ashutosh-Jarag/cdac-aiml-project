from pydantic import BaseModel, Field


# ---------- Classification ----------

class ClassificationRequest(BaseModel):
    title: str = Field(..., min_length=3)
    abstract: str = Field(..., min_length=10)


class ClassificationResponse(BaseModel):
    category: str
    confidence: float


# ---------- Publication Prediction ----------

class PublicationRequest(BaseModel):
    title: str
    abstract: str
    category: str
    author_count: int
    comment_length: int
    doi_exists: bool
    version_count: int


class PublicationResponse(BaseModel):
    published: bool
    probability: float


# ---------- Recommendation ----------

class RecommendationRequest(BaseModel):
    query: str
    top_k: int = Field(default=5, ge=1, le=20)


class RecommendedPaper(BaseModel):
    title: str
    similarity: float
    category: str
    paper_url: str


class RecommendationResponse(BaseModel):
    papers: list[RecommendedPaper]


# ---------- ML Chat ----------

class MLChatRequest(BaseModel):
    question: str
    provider: str | None = None
    api_key: str | None = None


class SourcePaper(BaseModel):
    title: str
    paper_url: str


class MLChatResponse(BaseModel):
    answer: str
    references: list[SourcePaper]