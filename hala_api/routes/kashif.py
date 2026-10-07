"""Kashif endpoint — فحص تسريبات (يستخدم hala-arab)"""

from fastapi import APIRouter, Depends, HTTPException, Request
from hala.commands.kashif import (
    detect_type,
    normalize_phone,
    scan_email,
    scan_phone,
)

from hala_api.auth import require_api_key
from hala_api.models.schemas import (
    BreachHit,
    KashifRequest,
    KashifResponse,
)
from hala_api.rate_limit import limiter

router = APIRouter(prefix="/kashif", tags=["kashif"])


@router.post("", response_model=KashifResponse)
@limiter.limit("30/minute")
async def kashif_scan(
    request: Request,
    req: KashifRequest,
    _: str = Depends(require_api_key),
) -> KashifResponse:
    """فحص إيميل أو رقم هاتف في تسريبات معروفة."""
    target = req.target.strip()
    target_type = detect_type(target)

    try:
        if target_type == "email":
            hits = await scan_email(target.lower())
            out_target = target.lower()
        else:
            e164 = normalize_phone(target, req.region)
            if not e164:
                raise HTTPException(
                    status_code=400,
                    detail="رقم غير صالح",
                )
            hits = await scan_phone(e164)
            out_target = e164
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # إزالة التكرار
    seen = set()
    unique_hits = []
    for h in hits:
        key = (h.get("name") or h.get("title") or "").lower()
        if key and key not in seen:
            seen.add(key)
            unique_hits.append(h)

    return KashifResponse(
        target=out_target,
        type=target_type,
        found=len(unique_hits) > 0,
        count=len(unique_hits),
        hits=[
            BreachHit(
                source=h.get("source", "unknown"),
                name=h.get("name"),
                title=h.get("title"),
                date=h.get("date"),
                records=h.get("records"),
                data_classes=h.get("data_classes", []),
            )
            for h in unique_hits
        ],
    )
