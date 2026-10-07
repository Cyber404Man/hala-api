"""HALA API — FastAPI app"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from hala_api.config import settings
from hala_api.routes import health, kashif, nlp, sitr


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "HALA API — Arabic-first threat intelligence.\n\n"
        "أول API عربي لفحص التسريبات، كشف الاحتيال، وحماية الخصوصية."
    ),
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes
app.include_router(health.router)
app.include_router(kashif.router, prefix=settings.api_prefix)
app.include_router(nlp.router, prefix=settings.api_prefix)
app.include_router(sitr.router, prefix=settings.api_prefix)


@app.get("/")
async def root():
    """نقطة البداية."""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "docs": "/docs",
        "health": "/health",
    }
