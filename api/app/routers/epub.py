from fastapi import APIRouter, Depends, HTTPException, UploadFile, status

from app.core.auth import get_current_user
from app.models.learning_path import EpubProgressUpdate, QuizSubmission
from app.services.epub_service import (
    count_epub_chapters,
    create_epub,
    get_epub,
    get_epub_download_url,
    get_epubs_for_path,
    update_progress,
    upload_epub_to_storage,
)
from app.services.quiz_service import generate_quiz, get_quizzes_for_epub, submit_quiz

router = APIRouter()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_epub(
    file: UploadFile,
    learning_path_id: str,
    user: dict = Depends(get_current_user),
):
    if not file.filename or not file.filename.endswith(".epub"):
        raise HTTPException(status_code=400, detail="Only .epub files are accepted")

    file_bytes = await file.read()
    total_chapters = count_epub_chapters(file_bytes)
    file_path = upload_epub_to_storage(file_bytes, file.filename, user["id"])

    return create_epub(
        user_id=user["id"],
        learning_path_id=learning_path_id,
        title=file.filename.replace(".epub", ""),
        file_path=file_path,
        total_chapters=total_chapters,
    )


@router.get("/path/{learning_path_id}")
async def get_path_epubs(
    learning_path_id: str,
    user: dict = Depends(get_current_user),
):
    return get_epubs_for_path(learning_path_id, user["id"])


@router.get("/{epub_id}")
async def get_epub_detail(
    epub_id: str,
    user: dict = Depends(get_current_user),
):
    epub = get_epub(epub_id, user["id"])
    if not epub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epub not found")

    download_url = get_epub_download_url(epub["file_path"])
    return {**epub, "download_url": download_url}


@router.put("/{epub_id}/progress")
async def update_epub_progress(
    epub_id: str,
    body: EpubProgressUpdate,
    user: dict = Depends(get_current_user),
):
    result = update_progress(epub_id, user["id"], body.current_chapter, body.progress_percent)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epub not found")
    return result


@router.get("/{epub_id}/quiz")
async def get_or_generate_quiz(
    epub_id: str,
    chapter: int,
    user: dict = Depends(get_current_user),
):
    """Get existing quiz for chapter or generate a new one."""
    epub = get_epub(epub_id, user["id"])
    if not epub:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Epub not found")

    existing = get_quizzes_for_epub(epub_id)
    for q in existing:
        if q["chapter"] == chapter:
            return q

    # For MVP: generate quiz with a placeholder chapter text prompt
    chapter_text = f"Kapitel {chapter} des Buches '{epub['title']}'"
    return generate_quiz(epub_id, chapter, chapter_text)


@router.post("/{epub_id}/quiz/{quiz_id}")
async def submit_quiz_answers(
    epub_id: str,
    quiz_id: str,
    body: QuizSubmission,
    _user: dict = Depends(get_current_user),
):
    try:
        return submit_quiz(quiz_id, body.answers)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
