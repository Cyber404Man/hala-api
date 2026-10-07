"""NLP endpoint — كشف الاحتيال (يستخدم hala-arab)"""
from fastapi import APIRouter, Depends, Request
from hala.commands.nlp import analyze  # ← الدالة الحقيقية من hala

from hala_api.auth import require_api_key
from hala_api.models.schemas import (
    NLPHit,
    NLPRequest,
    NLPResponse,
)
from hala_api.rate_limit import limiter

router = APIRouter(prefix="/nlp", tags=["nlp"])


@router.post("", response_model=NLPResponse)
@limiter.limit("60/minute")
async def analyze_text(
    request: Request,
    req: NLPRequest,
    _: str = Depends(require_api_key),
) -> NLPResponse:
    """كشف الاحتيال في رسالة عربية."""
    result = analyze(req.text)

    return NLPResponse(
        verdict=result["verdict"],
        score=result["score"],
        hits=[
            NLPHit(
                category=h[0],
                indicator=h[1],
                weight=h[2],
            )
            for h in result["hits"]
        ],
        dialects=result.get("dialects", []),
        urls=result.get("urls", []),
        phones=result.get("phones", []),
    )
