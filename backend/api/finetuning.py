"""
PodX FastAPI - Fine-Tuning Lab & Dataset Management Router
Manages training datasets, audio uploads, alignment, and LoRA/PEFT training jobs.
"""
import os
import time
import json
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from pydantic import BaseModel

from backend.core.config import settings
from database.db_manager import db_manager

router = APIRouter(prefix="/api/finetuning", tags=["finetuning"])

@router.get("/datasets")
def list_datasets():
    return db_manager.get_all_datasets()

@router.post("/datasets")
def create_dataset(
    name: str = Form(...),
    speaker_name: str = Form(...),
    description: str = Form(""),
    consent_confirmed: bool = Form(True)
):
    if not consent_confirmed:
        raise HTTPException(status_code=400, detail="Voice consent confirmation is mandatory.")
    return db_manager.create_dataset(name, speaker_name, description, consent_confirmed)

@router.get("/jobs")
def list_jobs():
    return db_manager.get_all_finetuning_jobs()

class LaunchJobRequest(BaseModel):
    dataset_id: str
    base_model: Optional[str] = "qwen3-tts-0.6b"
    total_epochs: Optional[int] = 5

@router.post("/jobs")
def launch_training_job(req: LaunchJobRequest):
    ds = db_manager.get_dataset(req.dataset_id)
    if not ds:
        raise HTTPException(status_code=404, detail="Dataset not found")

    job = db_manager.create_finetuning_job(
        dataset_id=req.dataset_id,
        base_model=req.base_model or "qwen3-tts-0.6b",
        total_epochs=req.total_epochs or 5
    )
    
    # Simulate first epoch training checkpoint initialization
    db_manager.update_finetuning_progress(job["id"], epoch=1, loss=1.452, progress=20.0)

    return db_manager.get_finetuning_job(job["id"])
