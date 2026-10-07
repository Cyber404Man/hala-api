"""API key authentication"""
from fastapi import Header, HTTPException, status

from hala_api.config import settings


async def require_api_key(
    x_api_key: str = Header(..., alias="X-API-Key"),
) -> str:
    """
    يتحقق من X-API-Key header.

    حاليًا: مفتاح واحد admin.
    لاحقًا: DB lookup + tiers.
    """
    if not x_api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="مفتاح API مطلوب (X-API-Key header)",
        )

    # مؤقتًا: مفتاح واحد
    if x_api_key != settings.admin_api_key:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="مفتاح API غير صالح",
        )

    return x_api_key
