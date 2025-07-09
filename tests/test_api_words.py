

def test_admin_can_add_word(client, register_and_login_admin):
    token = register_and_login_admin
    resp = client.post("/words/add", json={
        "id": 0, "text": "testword", "translation": "", "level": "",
        "type": "", "domain": "", "example": "", "audio_url": "", "normalized": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    assert resp.json()["text"] == "testword"

def test_learner_cannot_add_word(client, register_and_login_learner):
    token = register_and_login_learner
    resp = client.post("/words/add", json={
        "id": 0, "text": "forbidden", "translation": "", "level": "",
        "type": "", "domain": "", "example": "", "audio_url": "", "normalized": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_any_authenticated_user_can_list_words(client, register_and_login_learner):
    token = register_and_login_learner
    resp = client.get("/words/list", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200

def test_unauthenticated_cannot_list_words(client):
    resp = client.get("/words/list")
    assert resp.status_code == 401

def test_duplicate_word_addition_returns_error(client, register_and_login_admin):
    token = register_and_login_admin
    # Add once
    client.post("/words/add", json={
        "id": 0, "text": "duplicate", "translation": "", "level": "",
        "type": "", "domain": "", "example": "", "audio_url": "", "normalized": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    # Try to add again
    resp = client.post("/words/add", json={
        "id": 0, "text": "duplicate", "translation": "", "level": "",
        "type": "", "domain": "", "example": "", "audio_url": "", "normalized": "", "notes": ""
    }, headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code in (400, 409)  # Depending on your error handling
