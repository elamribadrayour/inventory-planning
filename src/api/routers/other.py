from fastapi import APIRouter
from fastapi.responses import ORJSONResponse


router = APIRouter(tags=["Other"])


@router.get("/")
async def read_root():
    return ORJSONResponse(content=dict())


@router.get("/health")
async def health():
    """
    Determine if the container is working and healthy
    """
    return ORJSONResponse(content=dict())
