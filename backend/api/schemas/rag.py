from pydantic import BaseModel


class ChatRequest(BaseModel):

    question: str


class SourcePaper(BaseModel):

    title: str

    authors: str

    category: str


class ChatResponse(BaseModel):

    answer: str

    sources: list[SourcePaper]