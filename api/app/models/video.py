from datetime import datetime

from pydantic import BaseModel


class Video(BaseModel):
    id: str
    source: str
    title: str
    url: str
    description: str | None = None
    published_at: datetime | None = None
    discovered_at: datetime


class VideoListResponse(BaseModel):
    videos: list[Video]
    total: int
