from fastapi import APIRouter

router = APIRouter()


@router.get("/", tags=["Healthcheck"], status_code=200)
async def read_root():
    """
    A healthcheck endpoint to check if the API is running.
    """
    return {"message": "API is running"}
