"""
PodX Core Configuration
Central configuration loaded from environment or defaults.
"""
import os
from pathlib import Path
from pydantic import BaseModel

BASE_DIR = Path(__file__).resolve().parent.parent.parent

class Settings(BaseModel):
    APP_NAME: str = "PodX — Elite Knowledge AI Podcast Studio"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    HOST: str = "127.0.0.1"
    PORT: int = 8000
    
    # Paths
    BASE_DIR: Path = BASE_DIR
    STORAGE_DIR: Path = BASE_DIR / "storage"
    AUDIO_DIR: Path = BASE_DIR / "storage" / "audio"
    PREVIEWS_DIR: Path = BASE_DIR / "storage" / "previews"
    DATASETS_DIR: Path = BASE_DIR / "storage" / "datasets"
    EXPORTS_DIR: Path = BASE_DIR / "storage" / "exports"
    CHECKPOINTS_DIR: Path = BASE_DIR / "storage" / "checkpoints"
    MODELS_DIR: Path = BASE_DIR / "models"
    DATABASE_PATH: Path = BASE_DIR / "storage" / "podx.db"
    
    # Audio Specs
    DEFAULT_SAMPLE_RATE: int = 24000
    MASTERING_SAMPLE_RATE: int = 48000
    TARGET_LUFS_STEREO: float = -16.0
    TARGET_LUFS_MONO: float = -19.0
    TRUE_PEAK_CEILING_DBTP: float = -1.0
    
    # Hardware & Performance
    DEVICE: str = "cuda"  # Auto-negotiated
    MAX_VRAM_MB: int = 3480
    ENABLE_OFFLOAD: bool = True
    DEFAULT_PROVIDER: str = "kokoro"
    FALLBACK_PROVIDER: str = "kokoro"
    
    # Generation Defaults
    DEFAULT_PAUSE_BETWEEN_SPEAKERS_SEC: float = 0.45
    MAX_CHUNK_CHARS: int = 380

settings = Settings()

# Ensure directories exist
for folder in [
    settings.STORAGE_DIR,
    settings.AUDIO_DIR,
    settings.PREVIEWS_DIR,
    settings.DATASETS_DIR,
    settings.EXPORTS_DIR,
    settings.CHECKPOINTS_DIR,
    settings.MODELS_DIR
]:
    folder.mkdir(parents=True, exist_ok=True)
