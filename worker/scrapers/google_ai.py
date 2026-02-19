import httpx
from bs4 import BeautifulSoup

from .base import BaseScraper, ScrapedVideo


class GoogleAIScraper(BaseScraper):
    source = "google_ai"
    BASE_URL = "https://ai.google/build/machine-learning/"

    async def scrape(self) -> list[ScrapedVideo]:
        videos: list[ScrapedVideo] = []
        try:
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                resp = await client.get(self.BASE_URL)
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.select("a[href*='cloud.google.com'], a[href*='developers.google']"):
                title = card.get_text(strip=True)
                href = card.get("href", "")
                if not title or not href or len(title) < 5:
                    continue

                url = href if href.startswith("http") else f"https://ai.google{href}"

                videos.append(
                    ScrapedVideo(
                        source=self.source,
                        title=title,
                        url=url,
                        description="",
                    )
                )
        except Exception as e:
            print(f"[{self.source}] Scraping failed: {e}")

        return videos
