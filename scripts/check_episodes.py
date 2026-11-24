import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.db_manager import db_manager

episodes = db_manager.get_all_episodes()
print(f"Total episodes in DB: {len(episodes)}")
for ep in episodes:
    print(f"ID: {ep['id']}")
    print(f"  Title: {ep['title']}")
    print(f"  Status: {ep['status']}")
    print(f"  Stage: {ep.get('current_stage')}")
    print(f"  Progress: {ep.get('progress_percent')}%")
    print(f"  Rendered Segments: {ep.get('rendered_segments')} / {ep.get('total_segments')}")
    print(f"  Duration: {ep.get('duration_seconds')}s")
    print(f"  Master WAV: {ep.get('master_wav_path')}")
    print(f"  Master MP3: {ep.get('master_mp3_path')}")
    print(f"  Error: {ep.get('error_message')}")
    print("-" * 50)
