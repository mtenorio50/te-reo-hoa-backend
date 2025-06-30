def test_list_words_authenticated_user(client):
    # Register & login as a normal user (not admin)
    reg = client.post("/users/register", json={
        "email": "learner2@example.com",
        "password": "pass"
    })
    login = client.post("/login/", data={
        "username": "learner2@example.com",
        "password": "pass"
    })
    token = login.json()["access_token"]

    # Try to list words (should be allowed)
    resp = client.get(
        "/words/list",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 200
    words = resp.json()
    assert isinstance(words, list)

def test_list_words_unauthenticated(client):
    resp = client.get("/words/list")
    assert resp.status_code == 401  # Unauthorized
