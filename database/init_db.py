"""
PodX Database Initialization & Voice Seeding Script
Creates all tables with SQLite WAL mode and seeds 24 unique voice profiles.
"""
import os
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import json
from database.session import engine, SessionLocal, Base
from database.models import VoiceProfile

def init_database():
    print("Creating database schema with WAL mode...")
    Base.metadata.create_all(bind=engine)
    print("Schema created successfully.")

    db = SessionLocal()
    try:
        # Check existing voice profiles
        existing_count = db.query(VoiceProfile).count()
        if existing_count >= 24:
            print(f"Voice profiles already seeded ({existing_count} voices).")
            return

        voices_json_path = Path(__file__).resolve().parent.parent / "configs" / "voice_profiles.json"
        if not voices_json_path.exists():
            print(f"Warning: {voices_json_path} not found.")
            return

        with open(voices_json_path, "r", encoding="utf-8") as f:
            voices_data = json.load(f)

        for v in voices_data:
            existing = db.query(VoiceProfile).filter(VoiceProfile.id == v["id"]).first()
            if not existing:
                vp = VoiceProfile(
                    id=v["id"],
                    name=v["name"],
                    gender=v["gender"],
                    accent=v["accent"],
                    language=v.get("language", "en-US"),
                    description=v.get("description", ""),
                    tags=v.get("tags", []),
                    pitch_offset=v.get("pitch_offset", 0.0),
                    speed_factor=v.get("speed_factor", 1.0),
                    preferred_provider=v.get("preferred_provider", "kokoro"),
                    provider_voice_id=v.get("provider_voice_id", "am_adam"),
                    is_custom=False
                )
                db.add(vp)
        db.commit()
        print(f"Successfully seeded {len(voices_data)} voice profiles into database.")
    except Exception as e:
        db.rollback()
        print(f"Error seeding database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    init_database()
