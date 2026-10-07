"""Sitr endpoint — روابط حذف (يستخدم hala-arab)"""
from fastapi import APIRouter, Depends, Query
from hala.utils import load_json

from hala_api.auth import require_api_key
from hala_api.models.schemas import SitrResponse, SitrSite

router = APIRouter(prefix="/sitr", tags=["sitr"])


@router.get("", response_model=SitrResponse)
async def list_sites(
    country: str | None = Query(None),
    type: str | None = Query(None, alias="type"),
    _: str = Depends(require_api_key),
) -> SitrResponse:
    """روابط حذف البيانات من مواقع عربية وعالمية."""
    data = load_json("optout_urls.json")
    sites = data.get("sites", [])

    if country:
        country_u = country.upper()
        sites = [
            s for s in sites
            if country_u in s.get("countries", [])
            or "ALL" in s.get("countries", [])
        ]

    if type:
        sites = [s for s in sites if s.get("type") == type]

    return SitrResponse(
        count=len(sites),
        sites=[SitrSite(**s) for s in sites],
    )
