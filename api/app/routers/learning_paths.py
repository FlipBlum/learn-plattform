from fastapi import APIRouter, Depends, HTTPException, status

from app.core.auth import get_current_user
from app.models.learning_path import LearningPathCreate, LearningPathUpdate
from app.services.learning_path_service import create_path, delete_path, list_paths, update_path

router = APIRouter()


@router.get("/")
async def get_learning_paths(user: dict = Depends(get_current_user)):
    return list_paths(user["id"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_learning_path(
    body: LearningPathCreate,
    user: dict = Depends(get_current_user),
):
    return create_path(user["id"], body.name, body.status.value)


@router.put("/{path_id}")
async def update_learning_path(
    path_id: str,
    body: LearningPathUpdate,
    user: dict = Depends(get_current_user),
):
    result = update_path(path_id, user["id"], body.model_dump(exclude_none=True))
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
    return result


@router.delete("/{path_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_learning_path(
    path_id: str,
    user: dict = Depends(get_current_user),
):
    if not delete_path(path_id, user["id"]):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Learning path not found")
