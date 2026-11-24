"""
PodX Workflow Verification Script
Tests end-to-end podcast generation pipeline with multi-speaker synthesis and mastering.
"""
import sys
import os
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database.db_manager import db_manager
from workflows.podcast_workflow import PodcastProductionWorkflow

def main():
    print("--- Starting PodX Workflow Verification ---")
    test_script = """PODCAST TITLE: Test Pilot - The Spark of Innovation
MODE: Two-host intellectual discussion
QUALITY: Studio

M01 [calm, thoughtful]: Innovation is not merely inventing something new. It is solving a human problem in an unforgettable way.

[pause: 1.0 second]

F01 [curious, analytical]: That is a vital distinction, Alexander. How does a creative team sustain that focus over time?

M01 [confident]: By protecting curiosity and embracing rigorous testing."""

    # Ensure voices are seeded
    db_manager.seed_default_voices("configs/voice_profiles.json")

    proj = db_manager.create_project(
        title="Test Pilot",
        raw_script=test_script,
        mode="two-host",
        quality_mode="Studio"
    )
    print(f"Project created: {proj['id']}")

    ep = db_manager.create_episode(project_id=proj['id'], title="Episode 1: The Spark of Innovation")
    print(f"Episode created: {ep['id']}")

    def on_progress(p):
        print(f"  [{p['stage']}] {p['progress']}% - {p['message']}")

    wf = PodcastProductionWorkflow(episode_id=ep['id'], progress_callback=on_progress)
    result = wf.execute()

    print("\n--- Generation Completed Successfully ---")
    print(f"Status: {result['status']}")
    print(f"Duration: {result['duration_seconds']} seconds")
    print(f"Integrated LUFS: {result['master_paths'].get('integrated_lufs'):.2f}")
    print(f"True Peak dBTP: {result['master_paths'].get('true_peak_dbtp'):.2f}")
    print(f"Master WAV: {result['master_paths'].get('wav')}")
    print(f"Master MP3: {result['master_paths'].get('mp3')}")
    print(f"SRT Subtitles: {result['master_paths'].get('srt')}")
    print(f"VTT Subtitles: {result['master_paths'].get('vtt')}")
    print(f"JSON Transcript: {result['master_paths'].get('json')}")
    print(f"QA Status: {result['qa_report'].get('status')}")

if __name__ == "__main__":
    main()
