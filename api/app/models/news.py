from datetime import date, datetime

from pydantic import BaseModel


class NewsSource(BaseModel):
    title: str | None = None
    url: str | None = None


class NewsPage(BaseModel):
    id: str
    date: date
    content: str
    sources: list[NewsSource]
    generated_at: datetime


class NewsListResponse(BaseModel):
    pages: list[NewsPage]
    total: int
