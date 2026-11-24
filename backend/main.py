"""
PodX Main Application Entrypoint
FastAPI server, CORS middleware, API routers, static audio assets, and SPA frontend serving.
"""
import os
import sys
from pathlib import Path

# Ensure project root is always on sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.core.config import settings
from backend.api.chat import router as chat_router
from backend.api.podcasts import router as podcasts_router
from backend.api.voices import router as voices_router
from backend.api.finetuning import router as finetuning_router
from backend.api.system import router as system_router
from database.db_manager import db_manager

# Ensure database is seeded with 24 voices
db_manager.seed_default_voices(str(settings.BASE_DIR / "configs" / "voice_profiles.json"))

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Autonomous Local AI Podcast Studio"
)

# Enable CORS for local Vite dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Register API Routers
app.include_router(chat_router)
app.include_router(podcasts_router)
app.include_router(voices_router)
app.include_router(finetuning_router)
app.include_router(system_router)

# Mount static audio directories for streaming
app.mount("/static/audio", StaticFiles(directory=str(settings.AUDIO_DIR)), name="static_audio")
app.mount("/static/exports", StaticFiles(directory=str(settings.EXPORTS_DIR)), name="static_exports")
app.mount("/static/previews", StaticFiles(directory=str(settings.PREVIEWS_DIR)), name="static_previews")

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

# Mount SPA frontend if dist exists
dist_dir = settings.BASE_DIR / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/assets", StaticFiles(directory=str(dist_dir / "assets")), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = dist_dir / full_path
        if file_path.exists() and file_path.is_file():
            return FileResponse(str(file_path))
        return FileResponse(str(dist_dir / "index.html"))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host="127.0.0.1", port=8001, reload=False)
