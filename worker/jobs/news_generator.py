from datetime import datetime, timedelta, timezone

from openai import OpenAI

from config import OPENAI_API_KEY
from db import get_supabase

SYSTEM_PROMPT = """Du bist ein Redakteur fuer eine personalisierte Lernplattform.
Deine Aufgabe ist es, aus den gesammelten Quellen (Newsletter, RSS-Feeds, Links)
eine taegliche Newspage zu erstellen.

Regeln:
- Schreibe auf Deutsch
- Umfang: ca. 10 A4-Seiten
- Strukturiere nach Themengebieten (KI/LLMs, Cloud, DevOps, Data Science etc.)
- Jeder Abschnitt hat eine Ueberschrift, Zusammenfassung und Quellenangaben
- Nutze Markdown-Formatierung
- Fokussiere auf die Lernpfade des Users: {learning_paths}
- Sei informativ und praezise, keine Fuellwoerter
- Verlinke Originalquellen"""


def _get_learning_paths() -> list[str]:
    sb = get_supabase()
    result = sb.table("learning_paths").select("name").execute()
    return [lp["name"] for lp in result.data] if result.data else [
        "KI-News", "Cloud Computing", "DevOps", "Data Science"
    ]


def _get_recent_sources(hours: int = 24) -> list[dict]:
    sb = get_supabase()
    since = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    result = (
        sb.table("news_sources")
        .select("*")
        .gte("fetched_at", since)
        .order("fetched_at", desc=True)
        .limit(100)
        .execute()
    )
    return result.data or []


def _build_source_text(sources: list[dict]) -> str:
    parts: list[str] = []
    for src in sources:
        entry = f"- [{src.get('source_type', 'unknown')}] {src.get('title', '')}"
        if src.get("content"):
            entry += f"\n  {src['content'][:500]}"
        if src.get("url"):
            entry += f"\n  URL: {src['url']}"
        if src.get("links"):
            entry += f"\n  Links: {', '.join(src['links'][:5])}"
        parts.append(entry)
    return "\n\n".join(parts)


def _generate_news_content(sources: list[dict], learning_paths: list[str]) -> str:
    client = OpenAI(api_key=OPENAI_API_KEY)
    source_text = _build_source_text(sources)
    paths_str = ", ".join(learning_paths)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT.format(learning_paths=paths_str),
            },
            {
                "role": "user",
                "content": f"Erstelle die taegliche Newspage basierend auf folgenden {len(sources)} Quellen:\n\n{source_text}",
            },
        ],
        max_tokens=8000,
        temperature=0.3,
    )

    return response.choices[0].message.content or ""


def run():
    """Generate daily personalized news page from collected sources."""
    print("Running news_generator job...")
    sources = _get_recent_sources()
    if not sources:
        print("No sources found for news generation")
        return

    learning_paths = _get_learning_paths()
    content = _generate_news_content(sources, learning_paths)
    if not content:
        print("News generation returned empty content")
        return

    sb = get_supabase()
    today = datetime.now(timezone.utc).date().isoformat()

    existing = sb.table("news_pages").select("id").eq("date", today).execute()
    if existing.data:
        sb.table("news_pages").update(
            {
                "content": content,
                "sources": [{"title": s.get("title"), "url": s.get("url")} for s in sources],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).eq("date", today).execute()
    else:
        sb.table("news_pages").insert(
            {
                "date": today,
                "content": content,
                "sources": [{"title": s.get("title"), "url": s.get("url")} for s in sources],
                "generated_at": datetime.now(timezone.utc).isoformat(),
            }
        ).execute()

    print(f"News page generated for {today} ({len(content)} chars)")
