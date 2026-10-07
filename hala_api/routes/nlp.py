"""NLP endpoint — كشف الاحتيال (يستخدم hala-arab)"""
from fastapi import APIRouter, Depends
from hala.commands.nlp import analyze  # ← الدالة الحقيقية من hala

from hala_api.auth import require_api_key
from hala_api.models.schemas import (
    NLPRequest, NLPResponse, NLPHit,
)

router = APIRouter(prefix="/nlp", tags=["nlp"])


@router.post("", response_model=NLPResponse)
async def analyze_text(
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
