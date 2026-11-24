"""
PodX Voice Library Preview Generator
Synthesizes 15-20 second acoustic preview samples for all 24 voice profiles.
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.core.config import settings
from database.db_manager import db_manager
from model_providers.manager import provider_manager
import soundfile as sf

def generate_all_previews():
    print("--- Generating Preview Samples for 24 Voices ---")
    voices = db_manager.get_all_voices()
    settings.PREVIEWS_DIR.mkdir(parents=True, exist_ok=True)

    for idx, v in enumerate(voices, start=1):
        vid = v["id"]
        vname = v["name"]
        preview_file = settings.PREVIEWS_DIR / f"preview_{vid}.wav"
        
        sample_script = (
            f"Hello and welcome. I am {vname}. "
            f"As a voice persona for PodX Studio, I specialize in {v.get('description', 'in-depth conversations and narratives')}. "
            f"Every episode is delivered with precision and natural expressive cadence."
        )

        voice_dict = {
            "preferred_provider": v.get("preferred_provider", "kokoro"),
            "provider_voice_id": v.get("provider_voice_id", "am_adam"),
            "edge_voice_id": v.get("edge_voice_id", "en-US-GuyNeural")
        }

        print(f"[{idx}/24] Synthesizing preview for {vid} ({vname})...")
        try:
            audio, sr = provider_manager.synthesize(
                text=sample_script,
                voice_profile=voice_dict,
                speed=v.get("speed_factor", 1.0),
                pitch=v.get("pitch_offset", 0.0)
            )
            sf.write(str(preview_file), audio, sr)
            
            # Update DB with path
            with db_manager.get_connection() as conn:
                conn.execute(
                    "UPDATE voice_profiles SET preview_audio_path = ? WHERE id = ?",
                    (str(preview_file), vid)
                )
                conn.commit()
            print(f"  -> Saved {preview_file.name} ({round(len(audio)/sr, 1)}s)")
        except Exception as e:
            print(f"  -> Error generating preview for {vid}: {e}")

    print("\nAll 24 voice previews generated and registered in SQLite database!")

if __name__ == "__main__":
    generate_all_previews()
