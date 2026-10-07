"""Health check endpoint"""
from fastapi import APIRouter
from hala_api.config import settings
from hala_api.models.schemas import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """فحص صحة الـAPI."""
    return HealthResponse(
        status="ok",
        version=settings.app_version,
        service=settings.app_name,
    )
