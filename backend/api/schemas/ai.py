from pydantic import BaseModel



# ---------- Chat ----------

class AIChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    provider: str | None = None
    api_key: str | None = None


class AIReference(BaseModel):

    text: str

    source: str

    page: int


class AIChatResponse(BaseModel):
    answer: str
    references: list[AIReference]


# ---------- Summary ----------

class SummaryRequest(BaseModel):
    session_id: str
    mode: str = "short"


class SummaryResponse(BaseModel):
    summary: str
    bullet_points: list[str]


# ---------- Upload ----------

class UploadResponse(BaseModel):
    session_id: str
    filename: str
    total_pages: int





class RenameChat(BaseModel):

    title: str