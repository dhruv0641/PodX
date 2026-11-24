"""
Unit and integration tests for PodX FastAPI Endpoints.
"""
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health_check():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"

def test_get_voices():
    res = client.get("/api/voices")
    assert res.status_code == 200
    voices = res.json()
    assert len(voices) >= 24
    voice_ids = [v["id"] for v in voices]
    assert "M01" in voice_ids
    assert "F01" in voice_ids

def test_hardware_status():
    res = client.get("/api/system/hardware")
    assert res.status_code == 200
    hw = res.json()
    assert "cpu" in hw
    assert "ram" in hw
    assert "gpu" in hw

def test_chat_conversational_response():
    res = client.post("/api/chat", json={"message": "Hello, how does PodX work?"})
    assert res.status_code == 200
    data = res.json()
    assert "reply" in data
    assert not data.get("is_podcast_job", False)
