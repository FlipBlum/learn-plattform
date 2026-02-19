from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def list_learning_paths():
    return {"message": "learning paths endpoint"}
