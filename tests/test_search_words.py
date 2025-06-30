def test_search_words(client, db_session):
    # 1. Register & login as admin to add a couple of words
    reg = client.post("/users/register", json={
        "email": "searchadmin@example.com",
        "password": "pass"
    })
    user_id = reg.json()["id"]
    from app.models import User
    user = db_session.query(User).filter_by(id=user_id).first()
    user.role = "admin"
    db_session.commit()
    login = client.post("/login/", data={
        "username": "searchadmin@example.com",
        "password": "pass"
    })
    admin_token = login.json()["access_token"]

    # Mocked AI is still active from previous test; add two words
    client.post("/words/add", json={
        "id": 0,
        "text": "love",
        "translation": "",
        "level": "",
        "type": "",
        "domain": "",
        "example": "",
        "audio_url": "",
        "normalized": "",
        "notes": ""
    }, headers={"Authorization": f"Bearer {admin_token}"})

    client.post("/words/add", json={
        "id": 0,
        "text": "courage",
        "translation": "",
        "level": "",
        "type": "",
        "domain": "",
        "example": "",
        "audio_url": "",
        "normalized": "",
        "notes": ""
    }, headers={"Authorization": f"Bearer {admin_token}"})

    # 2. Register & login as a normal user (not admin)
    reg2 = client.post("/users/register", json={
        "email": "searchlearner@example.com",
        "password": "pass"
    })
    login2 = client.post("/login/", data={
        "username": "searchlearner@example.com",
        "password": "pass"
    })
    user_token = login2.json()["access_token"]

    # 3. Search by word text
    resp = client.get(
        "/words/search",
        params={"search_by": "word", "value": "lov"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp.status_code == 200
    data = resp.json()
    assert any(w["text"].lower() == "love" for w in data)

    # 4. Search by level (should return both, since default is 'beginner' in our mock)
    resp2 = client.get(
        "/words/search",
        params={"search_by": "level", "value": "beginner"},
        headers={"Authorization": f"Bearer {user_token}"}
    )
    assert resp2.status_code == 200
    data2 = resp2.json()
    assert len(data2) >= 2
