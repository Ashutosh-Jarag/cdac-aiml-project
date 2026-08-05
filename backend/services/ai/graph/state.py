from typing import TypedDict
from sqlalchemy.orm import Session


class ChatState(TypedDict):

    db: Session

    session_id: str

    session_uuid: object

    provider: str

    api_key: str | None

    question: str

    history: str

    context: str

    answer: str

    references: list[dict]