# test for registration and duplicates

def test_user_registration(client):
    response = client.post("/users/register", json={
        "email": "uniqueuser@example.com",
        "password": "testpassword"
    })
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["email"] == "uniqueuser@example.com"
    assert "id" in data
    assert "role" in data


def test_duplicate_registration(client):
    # Register once
    resp1 = client.post("/users/register", json={
        "email": "dupeuser@example.com",
        "password": "secret"
    })
    assert resp1.status_code == 200

    # Register again with the same email
    resp2 = client.post("/users/register", json={
        "email": "dupeuser@example.com",
        "password": "secret"
    })
    assert resp2.status_code == 400, resp2.text  # Should get a 400 error
    data = resp2.json()
    assert "already registered" in data["detail"]
