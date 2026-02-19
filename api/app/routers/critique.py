from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def get_critique():
    return {"message": "critique endpoint"}
