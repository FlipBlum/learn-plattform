import httpx
from bs4 import BeautifulSoup

from .base import BaseScraper, ScrapedVideo


class DeepLearningAIScraper(BaseScraper):
    source = "deeplearning.ai"
    BASE_URL = "https://www.deeplearning.ai/courses/"

    async def scrape(self) -> list[ScrapedVideo]:
        videos: list[ScrapedVideo] = []
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                resp = await client.get(self.BASE_URL)
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.select("a[href*='/courses/']"):
                title_el = card.select_one("h2, h3, .card-title, span")
                title = title_el.get_text(strip=True) if title_el else card.get_text(strip=True)
                href = card.get("href", "")
                if not title or not href:
                    continue

                url = href if href.startswith("http") else f"https://www.deeplearning.ai{href}"
                desc_el = card.select_one("p, .card-description")
                description = desc_el.get_text(strip=True) if desc_el else ""

                videos.append(
                    ScrapedVideo(
                        source=self.source,
                        title=title,
                        url=url,
                        description=description,
                    )
                )
        except Exception as e:
            print(f"[{self.source}] Scraping failed: {e}")

        return videos
