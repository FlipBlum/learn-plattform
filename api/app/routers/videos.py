from fastapi import APIRouter, Depends, Query

from app.core.auth import get_current_user
from app.services.video_service import get_new_videos, list_videos

router = APIRouter()


@router.get("/")
async def get_videos(
    source: str | None = Query(None, description="Filter by source: deeplearning.ai, coursera, google_ai"),
    limit: int = Query(50, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _user: dict = Depends(get_current_user),
):
    return list_videos(source=source, limit=limit, offset=offset)


@router.get("/new")
async def get_new(
    days: int = Query(7, ge=1, le=30),
    _user: dict = Depends(get_current_user),
):
    return get_new_videos(days=days)
