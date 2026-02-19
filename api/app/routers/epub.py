from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_epub():
    return {"message": "epub endpoint"}
