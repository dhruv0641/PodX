"""
PodX FastAPI - Voice Library & AI Voice Designer Router
Serves 24 voice profiles, interactive previews, and natural-language voice design.
"""
import os
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
import soundfile as sf

from backend.core.config import settings
from database.db_manager import db_manager
from model_providers.manager import provider_manager

router = APIRouter(prefix="/api/voices", tags=["voices"])

@router.get("")
def get_voices():
    return db_manager.get_all_voices()

@router.get("/{voice_id}")
def get_voice(voice_id: str):
    v = db_manager.get_voice(voice_id)
    if not v:
        raise HTTPException(status_code=404, detail="Voice not found")
    return v

@router.get("/{voice_id}/preview")
def get_voice_preview(voice_id: str):
    """
    Streams or generates a 15-20 second preview audio sample for any voice profile.
    """
    v = db_manager.get_voice(voice_id)
    if not v:
        raise HTTPException(status_code=404, detail="Voice not found")

    preview_path = settings.PREVIEWS_DIR / f"preview_{voice_id}.wav"
    if not preview_path.exists():
        # Generate genuine preview sample on demand
        sample_text = (
            f"Hello, I am {v['name']}. This is a preview of my voice persona for PodX Studio. "
            f"I specialize in {v.get('description', 'engaging discussions and insightful analysis')}."
        )
        voice_dict = {
            "preferred_provider": v.get("preferred_provider", "kokoro"),
            "provider_voice_id": v.get("provider_voice_id", "am_adam"),
            "edge_voice_id": v.get("edge_voice_id", "en-US-GuyNeural")
        }
        audio_arr, sr = provider_manager.synthesize(
            text=sample_text,
            voice_profile=voice_dict,
            speed=v.get("speed_factor", 1.0),
            pitch=v.get("pitch_offset", 0.0)
        )
        sf.write(str(preview_path), audio_arr, sr)

    return FileResponse(str(preview_path), media_type="audio/wav")

class VoiceDesignRequest(BaseModel):
    name: str
    gender: str  # male, female, neutral
    accent: str  # American, British, Indian
    persona_prompt: str  # e.g. "A calm, intellectual philosopher with deep resonant baritone"
    speed: Optional[float] = 1.0
    pitch: Optional[float] = 0.0

@router.post("/design")
def design_new_voice(req: VoiceDesignRequest):
    """
    Creates an original voice profile from natural-language acoustic descriptions.
    """
    import uuid, time
    new_id = f"custom_{str(uuid.uuid4())[:8]}"
    
    # Map prompt cues to acoustic parameters
    prompt_lower = req.persona_prompt.lower()
    pitch = req.pitch or 0.0
    speed = req.speed or 1.0

    if "deep" in prompt_lower or "baritone" in prompt_lower:
        pitch -= 2.0
    elif "high" in prompt_lower or "youthful" in prompt_lower:
        pitch += 1.5

    if "fast" in prompt_lower or "energetic" in prompt_lower:
        speed += 0.08
    elif "slow" in prompt_lower or "deliberate" in prompt_lower or "calm" in prompt_lower:
        speed -= 0.06

    tags = ["custom", req.gender.lower(), req.accent.lower()]
    for cue in ["intellectual", "energetic", "calm", "cinematic", "friendly", "serious", "tech"]:
        if cue in prompt_lower:
            tags.append(cue)

    with db_manager.get_connection() as conn:
        conn.execute("""
        INSERT INTO voice_profiles (
            id, name, gender, accent, language, description, tags,
            pitch_offset, speed_factor, preferred_provider, provider_voice_id,
            edge_voice_id, is_custom, created_at
        ) VALUES (?, ?, ?, ?, 'en-US', ?, ?, ?, ?, 'kokoro', 'am_adam', 'en-US-GuyNeural', 1, ?)
        """, (
            new_id, req.name, req.gender, req.accent, req.persona_prompt,
            str(tags), pitch, speed, time.time()
        ))
        conn.commit()

    return db_manager.get_voice(new_id)
