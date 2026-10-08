from fastapi import APIRouter
from app.config import settings

router = APIRouter(prefix="/api", tags=["health"])


@router.get("/health")
async def health():
    return {"status": "ok", "model": settings.MODEL}
