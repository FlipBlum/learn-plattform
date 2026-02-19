from dataclasses import dataclass
from datetime import datetime


@dataclass
class ScrapedVideo:
    source: str
    title: str
    url: str
    description: str
    published_at: datetime | None = None


class BaseScraper:
    source: str = ""

    async def scrape(self) -> list[ScrapedVideo]:
        raise NotImplementedError
