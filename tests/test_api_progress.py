import pytest
from fastapi.testclient import TestClient


def test_learner_can_mark_word_learned(client, register_and_login_learner, register_and_login_admin, db_session, mock_get_translation):
    # Admin adds a word
    admin_token = register_and_login_admin
    resp = client.post("/words/add", json={
        "id": 0, "text": "progressword", "translation": "", "level": "",
        "type": "", "domain": "", "example": "", "audio_url": "", "normalized": "progressword", "notes": ""
    }, headers={"Authorization": f"Bearer {admin_token}"})
    word_id = resp.json()["id"]

    # Learner marks as learned
    learner_token = register_and_login_learner
    mark = client.post("/progress/word", json={
        "word_id": word_id, "status": "learned"
    }, headers={"Authorization": f"Bearer {learner_token}"})
    assert mark.status_code == 200
    assert mark.json()["status"] == "learned"


def test_cannot_mark_nonexistent_word_learned(client, register_and_login_learner):
    token = register_and_login_learner
    mark = client.post("/progress/word", json={
        "word_id": 9999, "status": "learned"
    }, headers={"Authorization": f"Bearer {token}"})
    assert mark.status_code == 404  # Should be 404 for non-existent word


def test_add_word_invalid_json(client, register_and_login_admin, mock_get_translation):
    token = register_and_login_admin

    # Test with missing required 'text' field
    resp = client.post("/words/add", json={
        "id": 0, "translation": "", "level": "", "type": "", "domain": "",
        "example": "", "audio_url": "", "normalized": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 422  # Should fail validation due to missing 'text'

    # Test with missing normalized field
    resp2 = client.post("/words/add", json={
        "id": 0, "text": "validtext", "translation": "", "level": "", "type": "",
        "domain": "", "example": "", "audio_url": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    # Should fail validation due to missing 'normalized'
    assert resp2.status_code == 422


def test_word_list_endpoint_exists(client, register_and_login_admin):
    # Test the actual existing endpoint instead of non-existent one
    token = register_and_login_admin
    resp = client.get(
        "/words/list", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200  # Should return empty list or existing words
