from datetime import datetime, timezone

import feedparser

from db import get_supabase

RSS_FEEDS = [
    {"name": "The Batch (deeplearning.ai)", "url": "https://www.deeplearning.ai/the-batch/feed/"},
    {"name": "OpenAI Blog", "url": "https://openai.com/blog/rss/"},
    {"name": "Google AI Blog", "url": "https://blog.google/technology/ai/rss/"},
    {"name": "MIT Technology Review AI", "url": "https://www.technologyreview.com/topic/artificial-intelligence/feed"},
    {"name": "Hacker News (AI)", "url": "https://hnrss.org/newest?q=AI+OR+LLM+OR+machine+learning&count=20"},
]


def run():
    """Fetch RSS feeds and store new entries in news_sources."""
    print("Running rss_fetcher job...")
    sb = get_supabase()
    now = datetime.now(timezone.utc).isoformat()
    total = 0

    for feed_config in RSS_FEEDS:
        try:
            feed = feedparser.parse(feed_config["url"])
            entries = feed.entries[:20]

            for entry in entries:
                link = entry.get("link", "")
                if not link:
                    continue
                existing = sb.table("news_sources").select("id").eq("url", link).execute()
                if existing.data:
                    continue

                published = entry.get("published_parsed")
                try:
                    published_at = (
                        datetime(*published[:6], tzinfo=timezone.utc).isoformat()
                        if published and len(published) >= 6
                        else None
                    )
                except (TypeError, ValueError):
                    published_at = None

                sb.table("news_sources").insert(
                    {
                        "source_type": "rss",
                        "title": entry.get("title", ""),
                        "content": entry.get("summary", ""),
                        "url": link,
                        "links": [link] if link else [],
                        "raw_data": {
                            "feed_name": feed_config["name"],
                            "author": entry.get("author", ""),
                        },
                        "published_at": published_at,
                        "fetched_at": now,
                    }
                ).execute()
                total += 1

        except Exception as e:
            print(f"RSS fetch failed for {feed_config['name']}: {e}")

    print(f"RSS fetcher: stored {total} new entries")
