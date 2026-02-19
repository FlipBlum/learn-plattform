from datetime import datetime, timezone

from openai import OpenAI

from app.core.config import settings
from app.services.supabase_client import get_supabase_admin

CRITIQUE_PROMPT = """Du bist ein sachlicher Lerncoach. Deine Aufgabe ist es, basierend auf den
Lernfortschrittsdaten eine ehrliche, motivierende Kritik zu verfassen.

Regeln:
- Sei sachlich und direkt, kein Schoenreden
- Benenne konkret, was gut laeuft und was nicht
- Gib konkrete Verbesserungsvorschlaege
- Motiviere zum Weitermachen, aber ohne leere Phrasen
- Schreibe auf Deutsch
- Nutze Markdown-Formatierung

Lernfortschritt:
{progress_data}"""


def _collect_progress_data(user_id: str) -> str:
    sb = get_supabase_admin()

    paths = sb.table("learning_paths").select("*").eq("user_id", user_id).execute()
    epubs = sb.table("epubs").select("*").eq("user_id", user_id).execute()
    quizzes_data: list[dict] = []
    for epub in epubs.data or []:
        qs = sb.table("quizzes").select("*").eq("epub_id", epub["id"]).execute()
        quizzes_data.extend(qs.data or [])

    lines: list[str] = []
    lines.append(f"Lernpfade: {len(paths.data or [])}")
    for p in paths.data or []:
        lines.append(f"  - {p['name']} (Status: {p['status']})")

    lines.append(f"\nBuecher: {len(epubs.data or [])}")
    for e in epubs.data or []:
        lines.append(
            f"  - {e['title']}: Kapitel {e['current_chapter']}/{e['total_chapters']} "
            f"({e['progress_percent']:.0f}%)"
        )

    if quizzes_data:
        taken = [q for q in quizzes_data if q.get("score") is not None]
        avg_score = sum(q["score"] for q in taken) / len(taken) if taken else 0
        lines.append(f"\nQuizzes absolviert: {len(taken)}")
        lines.append(f"Durchschnittliche Punktzahl: {avg_score:.1f}%")

    return "\n".join(lines)


def generate_critique(user_id: str, period: str = "weekly") -> dict:
    progress = _collect_progress_data(user_id)
    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "system",
                "content": CRITIQUE_PROMPT.format(progress_data=progress),
            },
            {
                "role": "user",
                "content": f"Erstelle eine {period} Kritik meines Lernverhaltens.",
            },
        ],
        max_tokens=2000,
        temperature=0.4,
    )

    content = response.choices[0].message.content or ""

    sb = get_supabase_admin()
    result = (
        sb.table("critiques")
        .insert(
            {
                "user_id": user_id,
                "period": period,
                "content": content,
                "created_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .execute()
    )

    return result.data[0]


def list_critiques(user_id: str) -> list[dict]:
    sb = get_supabase_admin()
    result = (
        sb.table("critiques")
        .select("*")
        .eq("user_id", user_id)
        .order("created_at", desc=True)
        .execute()
    )
    return result.data or []
