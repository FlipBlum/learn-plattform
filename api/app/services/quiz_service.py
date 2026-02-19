import json
from datetime import datetime, timezone

from openai import OpenAI

from app.core.config import settings
from app.services.supabase_client import get_supabase_admin

QUIZ_PROMPT = """Erstelle ein Quiz mit 5 Multiple-Choice-Fragen zum folgenden Buchkapitel.
Jede Frage hat 4 Antwortmoeglichkeiten. Genau eine ist korrekt.

Antworte ausschliesslich mit validem JSON in diesem Format:
{{
  "questions": [
    {{
      "question": "Die Frage",
      "options": ["A", "B", "C", "D"],
      "correct_index": 0
    }}
  ]
}}

Kapitelinhalt:
{chapter_text}"""


def generate_quiz(epub_id: str, chapter: int, chapter_text: str) -> dict:
    """Generate a quiz for a specific chapter using OpenAI."""
    client = OpenAI(api_key=settings.openai_api_key)

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[
            {
                "role": "user",
                "content": QUIZ_PROMPT.format(chapter_text=chapter_text[:6000]),
            },
        ],
        max_tokens=2000,
        temperature=0.5,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content or "{}"
    data = json.loads(content)

    sb = get_supabase_admin()
    result = (
        sb.table("quizzes")
        .insert(
            {
                "epub_id": epub_id,
                "chapter": chapter,
                "questions": data.get("questions", []),
            }
        )
        .execute()
    )

    return result.data[0]


def get_quiz(quiz_id: str) -> dict | None:
    sb = get_supabase_admin()
    result = sb.table("quizzes").select("*").eq("id", quiz_id).execute()
    return result.data[0] if result.data else None


def submit_quiz(quiz_id: str, answers: list[int]) -> dict:
    """Score a quiz submission and store results."""
    sb = get_supabase_admin()
    quiz_result = sb.table("quizzes").select("*").eq("id", quiz_id).execute()
    if not quiz_result.data:
        raise ValueError("Quiz not found")

    quiz = quiz_result.data[0]
    questions = quiz["questions"]
    correct = sum(
        1 for q, a in zip(questions, answers) if q.get("correct_index") == a
    )
    score = (correct / len(questions) * 100) if questions else 0

    sb.table("quizzes").update(
        {
            "answers": answers,
            "score": score,
            "taken_at": datetime.now(timezone.utc).isoformat(),
        }
    ).eq("id", quiz_id).execute()

    return {"quiz_id": quiz_id, "score": score, "correct": correct, "total": len(questions)}


def get_quizzes_for_epub(epub_id: str) -> list[dict]:
    sb = get_supabase_admin()
    result = (
        sb.table("quizzes")
        .select("*")
        .eq("epub_id", epub_id)
        .order("chapter")
        .execute()
    )
    return result.data or []
