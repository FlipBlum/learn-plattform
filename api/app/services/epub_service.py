from datetime import datetime, timezone

from app.services.supabase_client import get_supabase_admin


def get_epubs_for_path(learning_path_id: str, user_id: str) -> list[dict]:
    sb = get_supabase_admin()
    result = (
        sb.table("epubs")
        .select("*")
        .eq("learning_path_id", learning_path_id)
        .eq("user_id", user_id)
        .order("uploaded_at", desc=True)
        .execute()
    )
    return result.data or []


def get_epub(epub_id: str, user_id: str) -> dict | None:
    sb = get_supabase_admin()
    result = (
        sb.table("epubs")
        .select("*")
        .eq("id", epub_id)
        .eq("user_id", user_id)
        .execute()
    )
    return result.data[0] if result.data else None


def create_epub(
    user_id: str,
    learning_path_id: str,
    title: str,
    file_path: str,
    total_chapters: int,
) -> dict:
    sb = get_supabase_admin()
    result = (
        sb.table("epubs")
        .insert(
            {
                "user_id": user_id,
                "learning_path_id": learning_path_id,
                "title": title,
                "file_path": file_path,
                "total_chapters": total_chapters,
                "current_chapter": 0,
                "progress_percent": 0.0,
                "uploaded_at": datetime.now(timezone.utc).isoformat(),
            }
        )
        .execute()
    )
    if not result.data:
        raise RuntimeError("Failed to insert epub")
    return result.data[0]


def update_progress(epub_id: str, user_id: str, current_chapter: int, progress_percent: float) -> dict | None:
    sb = get_supabase_admin()
    result = (
        sb.table("epubs")
        .update(
            {
                "current_chapter": current_chapter,
                "progress_percent": min(progress_percent, 100.0),
            }
        )
        .eq("id", epub_id)
        .eq("user_id", user_id)
        .execute()
    )
    return result.data[0] if result.data else None


def upload_epub_to_storage(file_bytes: bytes, filename: str, user_id: str) -> str:
    """Upload epub file to Supabase Storage and return the file path."""
    sb = get_supabase_admin()
    path = f"{user_id}/{filename}"
    sb.storage.from_("epubs").upload(path, file_bytes, {"content-type": "application/epub+zip"})
    return path


def get_epub_download_url(file_path: str) -> str:
    """Generate a signed URL for downloading an epub."""
    sb = get_supabase_admin()
    result = sb.storage.from_("epubs").create_signed_url(file_path, 3600)
    return result.get("signedURL", "")


def count_epub_chapters(file_bytes: bytes) -> int:
    """Extract the number of chapters from an epub file."""
    try:
        import io

        import ebooklib
        from ebooklib import epub

        book = epub.read_epub(io.BytesIO(file_bytes))
        chapters = [
            item
            for item in book.get_items()
            if item.get_type() == ebooklib.ITEM_DOCUMENT
        ]
        return max(len(chapters), 1)
    except Exception:
        return 1
