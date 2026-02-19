from fastapi import APIRouter, Depends, Query

from app.core.auth import get_current_user
from app.services.critique_service import generate_critique, list_critiques

router = APIRouter()


@router.get("/")
async def get_critiques(user: dict = Depends(get_current_user)):
    return list_critiques(user["id"])


@router.post("/generate")
async def create_critique(
    period: str = Query("weekly", description="weekly or monthly"),
    user: dict = Depends(get_current_user),
):
    return generate_critique(user["id"], period)
