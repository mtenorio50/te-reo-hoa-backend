import pytest


@pytest.fixture(autouse=True)
def mock_get_translation(monkeypatch):
    async def fake_get_translation(word, max_retries=3):
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": '{"translation": "arohi", "type": "noun", "domain": "emotion", "example": "He aroha tēnei.", "notes": ""}'
                    }]
                }
            }]
        }
    monkeypatch.setattr(
        "app.ai_integration.get_translation", fake_get_translation)


def test_word_of_the_day(client, db_session):
    # Register & promote admin
    reg = client.post("/users/register", json={
        "email": "wotdadmin@example.com",
        "password": "pass"
    })
    user_id = reg.json()["id"]
    from app.models import User
    user = db_session.query(User).filter_by(id=user_id).first()
    user.role = "admin"
    db_session.commit()
    login = client.post("/login/", data={
        "username": "wotdadmin@example.com",
        "password": "pass"
    })
    admin_token = login.json()["access_token"]

    # Add a word
    client.post("/words/add", json={
        "id": 0,
        "text": "peace",
        "translation": "",
        "level": "",
        "type": "",
        "domain": "",
        "example": "",
        "audio_url": "",
        "normalized": "",
        "notes": ""
    }, headers={"Authorization": f"Bearer {admin_token}"})

    # Register & login as normal user
    reg2 = client.post("/users/register", json={
        "email": "wotduser@example.com",
        "password": "pass"
    })
    login2 = client.post("/login/", data={
        "username": "wotduser@example.com",
        "password": "pass"
    })
    user_token = login2.json()["access_token"]

    # Get word of the day as normal user
    resp = client.get(
        "/words/word_of_the_day",
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp.status_code == 200
    wotd = resp.json()
    assert wotd["text"].lower() == "peace"
    assert wotd["translation"] == "arohi"
