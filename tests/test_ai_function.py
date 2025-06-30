import pytest

@pytest.fixture(autouse=True)
def mock_get_translation(monkeypatch):
    async def fake_get_translation(word, max_retries=3):
        # Return fake Gemini-like result structure
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": '{"translation": "arohi", "type": "noun", "domain": "emotion", "example": "He aroha tēnei.", "notes": ""}'
                    }]
                }
            }]
        }
    monkeypatch.setattr("app.ai_integration.get_translation", fake_get_translation)

#admin only
def test_add_word(client, db_session):
    # Register & promote to admin
    reg = client.post("/users/register", json={
        "email": "addwordadmin@example.com",
        "password": "pass"
    })
    user_id = reg.json()["id"]
    from app.models import User
    user = db_session.query(User).filter_by(id=user_id).first()
    user.role = "admin"
    db_session.commit()

    login = client.post("/login/", data={
        "username": "addwordadmin@example.com",
        "password": "pass"
    })
    token = login.json()["access_token"]

    # Add a word
    resp = client.post(
        "/words/add",
        json={
            "id": 0,  # Can be 0 or omitted since the schema accepts it but ignores it
            "text": "love",
            "translation": "",
            "level": "",
            "type": "",
            "domain": "",
            "example": "",
            "audio_url": "",
            "normalized": "",
            "notes": ""
        },
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200, resp.text
    word = resp.json()
    assert word["text"].lower() == "love"
    assert word["translation"] == "arohi"
