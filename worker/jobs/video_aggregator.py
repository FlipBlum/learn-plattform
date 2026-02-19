import asyncio
from datetime import datetime, timezone

from db import get_supabase
from scrapers import CourseraScraper, DeepLearningAIScraper, GoogleAIScraper, ScrapedVideo


async def _aggregate() -> list[ScrapedVideo]:
    scrapers = [DeepLearningAIScraper(), CourseraScraper(), GoogleAIScraper()]
    all_videos: list[ScrapedVideo] = []
    for scraper in scrapers:
        videos = await scraper.scrape()
        print(f"[{scraper.source}] Found {len(videos)} videos")
        all_videos.extend(videos)
    return all_videos


def _store_videos(videos: list[ScrapedVideo]) -> int:
    sb = get_supabase()
    inserted = 0
    for video in videos:
        existing = sb.table("videos").select("id").eq("url", video.url).execute()
        if existing.data:
            continue

        sb.table("videos").insert(
            {
                "source": video.source,
                "title": video.title,
                "url": video.url,
                "description": video.description,
                "published_at": video.published_at.isoformat() if video.published_at else None,
                "discovered_at": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()
        inserted += 1

    return inserted


def run():
    """Aggregate videos from configured sources."""
    print("Running video_aggregator job...")
    videos = asyncio.run(_aggregate())
    inserted = _store_videos(videos)
    print(f"Video aggregation complete: {inserted} new videos stored")
