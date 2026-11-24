"""
PodX FastAPI - Chat & Script Ingestion Router
Accepts conversational prompts and automatically parses and triggers podcast production.
"""
import time
import uuid
from typing import Dict, Any, Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel

from database.db_manager import db_manager
from audio_engine.script_parser import ScriptParser
from workflows.podcast_workflow import PodcastProductionWorkflow

router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    conversation_id: Optional[str] = None
    message: str
    mode: Optional[str] = "two-host"
    quality_mode: Optional[str] = "Studio"
    speaker_mapping: Optional[Dict[str, str]] = None

# Active background generation runners
active_jobs: Dict[str, Any] = {}

def run_workflow_job(episode_id: str):
    try:
        wf = PodcastProductionWorkflow(episode_id)
        active_jobs[episode_id] = wf
        wf.execute()
    except Exception as e:
        print(f"[Background Job Error for {episode_id}] {e}")
    finally:
        active_jobs.pop(episode_id, None)

@router.get("/conversations")
def list_conversations():
    return db_manager.get_all_conversations()

@router.get("/conversations/{cid}")
def get_conversation(cid: str):
    conv = db_manager.get_conversation(cid)
    if not conv:
        raise HTTPException(status_code=404, detail="Conversation not found")
    return conv

@router.post("")
def handle_chat_message(req: ChatRequest, background_tasks: BackgroundTasks):
    cid = req.conversation_id
    if not cid:
        new_conv = db_manager.create_conversation("Studio Podcast Session")
        cid = new_conv["id"]

    # Record user message in DB
    user_msg = db_manager.add_message(cid, "user", req.message)

    # Detect if user message is a script submission
    is_script = False
    indicators = [
        "PODCAST TITLE:", "TITLE:", "MODE:", "M01:", "M01 [", "F01:", "F01 [",
        "Alexander:", "Sophia:", "HOST 1:", "HOST 2:", "[pause:"
    ]
    if any(ind.lower() in req.message.lower() for ind in indicators) or len(req.message.splitlines()) >= 3:
        is_script = True

    if is_script:
        # 1. Parse script
        parsed = ScriptParser.parse(req.message)
        
        # 2. Create project
        proj = db_manager.create_project(
            title=parsed.title,
            raw_script=req.message,
            conversation_id=cid,
            mode=req.mode or parsed.mode,
            quality_mode=req.quality_mode or parsed.quality_mode,
            speaker_mapping=req.speaker_mapping or {}
        )

        # 3. Create episode
        ep = db_manager.create_episode(proj["id"], parsed.title)

        # 4. Enqueue background generation
        background_tasks.add_task(run_workflow_job, ep["id"])

        reply_content = (
            f"🎙️ **Podcast Production Initialized!**\n\n"
            f"**Title**: {parsed.title}\n"
            f"**Mode**: {parsed.mode.title()}\n"
            f"**Speakers Detected**: {', '.join(parsed.speakers_detected) if parsed.speakers_detected else 'Alexander & Sophia'}\n"
            f"**Estimated Duration**: ~{round(parsed.estimated_duration_sec / 60, 1)} minutes ({parsed.total_segments} dialogue chunks)\n"
            f"**Quality Target**: {parsed.quality_mode} (-16 LUFS broadcast standard)\n\n"
            f"Production is now streaming in the background. You can track live telemetry below or in the **Podcast Studio** view."
        )

        assistant_msg = db_manager.add_message(
            cid, "assistant", reply_content, intent="script_submitted",
            metadata={
                "project_id": proj["id"],
                "episode_id": ep["id"],
                "speakers": parsed.speakers_detected,
                "total_segments": parsed.total_segments,
                "estimated_duration_sec": parsed.estimated_duration_sec
            }
        )

        return {
            "conversation_id": cid,
            "reply": reply_content,
            "project_id": proj["id"],
            "episode_id": ep["id"],
            "is_podcast_job": True,
            "estimated_duration_sec": parsed.estimated_duration_sec,
            "total_segments": parsed.total_segments
        }

    else:
        # Conversational query or directive
        reply = (
            "Welcome to **Elite Knowledge — AI Podcast Studio**.\n\n"
            "You can paste your complete multi-speaker script here, including stage directions like `[calm, thoughtful]` "
            "and pauses like `[pause: 1.5s]`. The studio will automatically isolate speakers, strip stage directions from dialogue, "
            "synthesize multi-track audio with 24 distinct voices, and apply broadcast-grade mastering (-16 LUFS, true peak limiting).\n\n"
            "Paste your script whenever you are ready!"
        )
        assistant_msg = db_manager.add_message(cid, "assistant", reply, intent="general_chat")
        return {
            "conversation_id": cid,
            "reply": reply,
            "is_podcast_job": False
        }
