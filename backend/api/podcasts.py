"""
PodX FastAPI - Podcast Projects & Episodes Router
Provides status, SSE live telemetry streams, segment regeneration, and multi-format downloads.
"""
import os
import json
import asyncio
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks, Response
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel

from backend.core.config import settings
from database.db_manager import db_manager
from model_providers.manager import provider_manager
import soundfile as sf

router = APIRouter(prefix="/api/podcasts", tags=["podcasts"])

@router.get("")
def list_episodes():
    return db_manager.get_all_episodes()

@router.get("/{episode_id}")
def get_episode_details(episode_id: str):
    ep = db_manager.get_episode(episode_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Episode not found")
    proj = db_manager.get_project(ep["project_id"])
    return {
        "episode": ep,
        "project": proj
    }

@router.get("/{episode_id}/progress")
async def stream_episode_progress(episode_id: str):
    """
    Server-Sent Events (SSE) live progress feed for front-end visualizers.
    """
    async def event_generator():
        last_progress = -1.0
        while True:
            ep = db_manager.get_episode(episode_id)
            if not ep:
                yield f"data: {json.dumps({'error': 'Episode not found'})}\n\n"
                break

            current_progress = ep.get("progress_percent", 0.0)
            status = ep.get("status", "pending")
            stage = ep.get("current_stage", "Queued")

            # Push event if progress changed or status is final
            payload = {
                "episode_id": episode_id,
                "status": status,
                "stage": stage,
                "progress": current_progress,
                "rendered_segments": ep.get("rendered_segments", 0),
                "total_segments": ep.get("total_segments", 0),
                "duration_seconds": ep.get("duration_seconds", 0.0),
                "error": ep.get("error_message")
            }
            yield f"data: {json.dumps(payload)}\n\n"

            if status in ["completed", "failed"]:
                break

            await asyncio.sleep(1.0)

    return StreamingResponse(event_generator(), media_type="text/event-stream")

class RegenerateSegmentRequest(BaseModel):
    spoken_text: Optional[str] = None
    voice_profile_id: Optional[str] = None
    pace: Optional[float] = 1.0
    pitch: Optional[float] = 0.0
    emotion: Optional[str] = "neutral"

@router.post("/{episode_id}/segments/{segment_id}/regenerate")
def regenerate_segment(episode_id: str, segment_id: str, req: RegenerateSegmentRequest):
    """
    Selectively re-synthesizes an individual dialogue segment without re-rendering the full podcast.
    """
    ep = db_manager.get_episode(episode_id)
    if not ep:
        raise HTTPException(status_code=404, detail="Episode not found")

    target_seg = None
    for s in ep.get("segments", []):
        if s["id"] == segment_id:
            target_seg = s
            break

    if not target_seg:
        raise HTTPException(status_code=404, detail="Segment not found")

    vp_id = req.voice_profile_id or target_seg["voice_profile_id"]
    vp = db_manager.get_voice(vp_id)
    voice_dict = {
        "preferred_provider": vp.get("preferred_provider", "kokoro") if vp else "kokoro",
        "provider_voice_id": vp.get("provider_voice_id", "am_adam") if vp else "am_adam",
        "edge_voice_id": vp.get("edge_voice_id", "en-US-GuyNeural") if vp else "en-US-GuyNeural"
    }

    text_to_speak = req.spoken_text or target_seg["spoken_text"]
    audio_arr, sr = provider_manager.synthesize(
        text=text_to_speak,
        voice_profile=voice_dict,
        speed=req.pace or target_seg.get("pace", 1.0),
        pitch=req.pitch or target_seg.get("pitch", 0.0),
        emotion=req.emotion or target_seg.get("emotion", "neutral")
    )

    seg_filename = f"seg_{episode_id}_{target_seg['sequence_index']:04d}.wav"
    seg_path = str(settings.AUDIO_DIR / seg_filename)
    sf.write(seg_path, audio_arr, sr)

    duration_sec = round(len(audio_arr) / sr, 3)
    db_manager.update_segment_rendered(segment_id, seg_path, duration_sec)

    return {
        "status": "regenerated",
        "segment_id": segment_id,
        "audio_path": seg_path,
        "duration_sec": duration_sec
    }

@router.get("/{episode_id}/audio")
def stream_master_audio(episode_id: str):
    ep = db_manager.get_episode(episode_id)
    if not ep or ep.get("status") != "completed":
        raise HTTPException(status_code=404, detail="Master audio not yet ready")

    # Prefer MP3 for browser streaming, fallback to WAV
    audio_file = ep.get("master_mp3_path") or ep.get("master_wav_path")
    if not audio_file or not os.path.exists(audio_file):
        raise HTTPException(status_code=404, detail="Audio file not found on disk")

    media_type = "audio/mpeg" if audio_file.endswith(".mp3") else "audio/wav"
    return FileResponse(audio_file, media_type=media_type)

@router.get("/{episode_id}/download/{fmt}")
def download_artifact(episode_id: str, fmt: str):
    ep = db_manager.get_episode(episode_id)
    if not ep or ep.get("status") != "completed":
        raise HTTPException(status_code=404, detail="Episode not ready")

    file_map = {
        "wav": ep.get("master_wav_path"),
        "mp3": ep.get("master_mp3_path"),
        "srt": ep.get("srt_path"),
        "vtt": ep.get("vtt_path"),
        "json": ep.get("transcript_json_path")
    }
    file_path = file_map.get(fmt.lower())
    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail=f"Format {fmt} not found")

    filename = f"PodX_{ep['title'].replace(' ', '_')}.{fmt.lower()}"
    return FileResponse(file_path, filename=filename)
