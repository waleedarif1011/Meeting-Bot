"""Tests for Flask API endpoints."""

import pytest

from server import SAMPLE_TRANSCRIPT, app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"


def test_sample(client):
    response = client.get("/sample")
    assert response.status_code == 200
    data = response.get_json()
    assert "transcript" in data
    assert "Attendees" in data["transcript"]
    assert data["transcript"] == SAMPLE_TRANSCRIPT


def test_upload_requires_fields(client):
    response = client.post("/upload", json={})
    assert response.status_code == 400


def test_upload_and_chat(client):
    session_id = "pytest_session_1"

    upload = client.post(
        "/upload",
        json={"transcript": SAMPLE_TRANSCRIPT, "session_id": session_id},
    )
    assert upload.status_code == 200
    assert "successfully" in upload.get_json()["message"].lower()

    chat = client.post(
        "/chat",
        json={"message": "Who participated in this meeting?", "session_id": session_id},
    )
    assert chat.status_code == 200
    reply = chat.get_json()["response"]
    assert "Sarah" in reply
    assert "Mike" in reply


def test_chat_missing_session(client):
    response = client.post(
        "/chat",
        json={"message": "Summarize", "session_id": "does_not_exist"},
    )
    assert response.status_code == 404


def test_chat_requires_fields(client):
    response = client.post("/chat", json={"message": "hi"})
    assert response.status_code == 400
