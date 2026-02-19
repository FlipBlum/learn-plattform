import httpx
from bs4 import BeautifulSoup

from .base import BaseScraper, ScrapedVideo


class CourseraScraper(BaseScraper):
    source = "coursera"
    SEARCH_URL = "https://www.coursera.org/search?query=artificial+intelligence&topic=Data%20Science&topic=Computer%20Science"

    async def scrape(self) -> list[ScrapedVideo]:
        videos: list[ScrapedVideo] = []
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
            }
            async with httpx.AsyncClient(timeout=30, follow_redirects=True) as client:
                resp = await client.get(self.SEARCH_URL, headers=headers)
                resp.raise_for_status()

            soup = BeautifulSoup(resp.text, "html.parser")
            for card in soup.select("a[href*='/learn/'], a[href*='/specializations/']"):
                title = card.get_text(strip=True)
                href = card.get("href", "")
                if not title or not href or len(title) < 5:
                    continue

                url = href if href.startswith("http") else f"https://www.coursera.org{href}"

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
