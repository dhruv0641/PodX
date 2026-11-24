"""
Unit tests for PodX SQLite WAL Database Engine.
"""
import os
import pytest
from database.db_manager import DatabaseManager

@pytest.fixture
def test_db(tmp_path):
    db_file = str(tmp_path / "test_podx.db")
    mgr = DatabaseManager(db_file)
    return mgr

def test_wal_mode_enabled(test_db):
    with test_db.get_connection() as conn:
        row = conn.execute("PRAGMA journal_mode;").fetchone()
        assert row[0].lower() == "wal"

def test_create_and_retrieve_project(test_db):
    proj = test_db.create_project(
        title="Test Architectural Evolution",
        raw_script="M01: Deep system design requires decoupled components."
    )
    assert proj["title"] == "Test Architectural Evolution"
    
    retrieved = test_db.get_project(proj["id"])
    assert retrieved is not None
    assert retrieved["title"] == proj["title"]

def test_episode_lifecycle(test_db):
    proj = test_db.create_project(title="Lifecycle Test", raw_script="M01: Test dialogue.")
    ep = test_db.create_episode(proj["id"], "Test Episode 1")
    assert ep["status"] == "pending"

    test_db.update_episode_status(ep["id"], "generating", 50.0, "Speech Generation")
    updated = test_db.get_episode(ep["id"])
    assert updated["status"] == "generating"
    assert updated["progress_percent"] == 50.0

    test_db.update_episode_completion(
        eid=ep["id"],
        duration_sec=120.5,
        master_wav="/storage/exports/test.wav",
        master_mp3="/storage/exports/test.mp3",
        srt="/storage/exports/test.srt",
        vtt="/storage/exports/test.vtt",
        json_path="/storage/exports/test.json",
        lufs=-16.0,
        peak=-1.0,
        qa_report={"status": "passed"}
    )
    final_ep = test_db.get_episode(ep["id"])
    assert final_ep["status"] == "completed"
    assert final_ep["duration_seconds"] == 120.5
    assert final_ep["integrated_lufs"] == -16.0
