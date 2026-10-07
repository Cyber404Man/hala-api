"""Pydantic schemas للـAPI"""
from __future__ import annotations

from pydantic import BaseModel, Field

# ─── Common ────────────────────────────────────────────

class HealthResponse(BaseModel):
    status: str
    version: str
    service: str


# ─── Kashif ────────────────────────────────────────────

class KashifRequest(BaseModel):
    target: str = Field(..., description="إيميل أو رقم هاتف")
    region: str = Field("PS", description="كود الدولة للأرقام")


class BreachHit(BaseModel):
    source: str
    name: str | None = None
    title: str | None = None
    date: str | None = None
    records: int | None = None
    data_classes: list[str] = []


class KashifResponse(BaseModel):
    target: str
    type: str  # email | phone
    found: bool
    count: int
    hits: list[BreachHit]


# ─── NLP ───────────────────────────────────────────────

class NLPRequest(BaseModel):
    text: str = Field(..., min_length=1, max_length=5000)


class NLPHit(BaseModel):
    category: str
    indicator: str
    weight: int


class NLPResponse(BaseModel):
    verdict: str  # SCAM | SUSPICIOUS | CLEAN
    score: int
    hits: list[NLPHit]
    dialects: list[tuple[str, int, str]] = []
    urls: list[str] = []
    phones: list[str] = []


# ─── Sitr ──────────────────────────────────────────────

class SitrSite(BaseModel):
    id: str
    name: str
    desc: str
    url: str
    countries: list[str]
    type: str
    difficulty: str


class SitrResponse(BaseModel):
    count: int
    sites: list[SitrSite]


# ─── Error ─────────────────────────────────────────────

class ErrorResponse(BaseModel):
    detail: str
