"""
PodX FastAPI - System Hardware & Model Manager Router
Monitors hardware, VRAM, RAM, disk space, and installed audio models.
"""
import os
import shutil
import psutil
from fastapi import APIRouter
from backend.core.config import settings
from scripts.detect_hardware import get_gpu_info, get_system_memory

router = APIRouter(prefix="/api/system", tags=["system"])

@router.get("/hardware")
def get_live_hardware_status():
    gpu = get_gpu_info()
    ram_total, ram_free = get_system_memory()
    d_disk = shutil.disk_usage(str(settings.BASE_DIR))

    cpu_pct = psutil.cpu_percent(interval=None)
    ram_pct = psutil.virtual_memory().percent

    return {
        "cpu": {
            "percent": cpu_pct,
            "cores": psutil.cpu_count(logical=True)
        },
        "ram": {
            "total_gb": ram_total,
            "free_gb": ram_free,
            "percent": ram_pct
        },
        "gpu": gpu,
        "storage": {
            "free_gb": round(d_disk.free / (1024**3), 2),
            "total_gb": round(d_disk.total / (1024**3), 2)
        }
    }

@router.get("/models")
def get_installed_models():
    kokoro_onnx = settings.MODELS_DIR / "kokoro" / "kokoro-v0_19.onnx"
    kokoro_voices = settings.MODELS_DIR / "kokoro" / "voices.json"

    return [
        {
            "id": "kokoro-82m",
            "name": "Kokoro-82M (Studio Production)",
            "family": "Kokoro",
            "installed": kokoro_onnx.exists() and kokoro_voices.exists(),
            "size_mb": round((kokoro_onnx.stat().st_size + kokoro_voices.stat().st_size) / (1024*1024), 1) if kokoro_onnx.exists() else 0,
            "vram_requirement_mb": 300,
            "recommended_modes": ["Fast Preview", "Balanced Quality", "Studio Quality"]
        },
        {
            "id": "edge-neural",
            "name": "Neural Broadcast Engine",
            "family": "Neural Multi-Accent",
            "installed": True,
            "size_mb": 0,
            "vram_requirement_mb": 0,
            "recommended_modes": ["Balanced Quality", "Studio Quality"]
        },
        {
            "id": "qwen3-tts-0.6b",
            "name": "Qwen3-TTS 0.6B CustomVoice",
            "family": "Qwen3-TTS",
            "installed": True,
            "size_mb": 1200,
            "vram_requirement_mb": 1600,
            "recommended_modes": ["Studio Quality", "Extreme Quality"]
        }
    ]
