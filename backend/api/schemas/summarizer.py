from enum import Enum

from pydantic import BaseModel


class SummaryStyle(str, Enum):
    BULLET = "bullet"
    SHORT = "short"
    DETAILED = "detailed"


class SummaryRequest(BaseModel):

    text: str

    style: SummaryStyle = SummaryStyle.BULLET


class SummaryResponse(BaseModel):

    summary: str