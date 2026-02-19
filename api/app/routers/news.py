from datetime import date

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.core.auth import get_current_user
from app.services.news_service import get_latest_news, get_news_by_date, list_news_pages

router = APIRouter()


@router.get("/")
async def get_news_list(
    limit: int = Query(30, ge=1, le=100),
    offset: int = Query(0, ge=0),
    _user: dict = Depends(get_current_user),
):
    return list_news_pages(limit=limit, offset=offset)


@router.get("/latest")
async def get_latest(
    _user: dict = Depends(get_current_user),
):
    page = get_latest_news()
    if not page:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No news available")
    return page


@router.get("/{target_date}")
async def get_by_date(
    target_date: date,
    _user: dict = Depends(get_current_user),
):
    page = get_news_by_date(target_date)
    if not page:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No news for {target_date}",
        )
    return page
