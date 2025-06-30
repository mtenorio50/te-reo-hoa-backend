# login test

def test_login_success(client):
    # Register user first
    reg_resp = client.post("/users/register", json={
        "email": "logintest@example.com",
        "password": "testpass"
    })
    assert reg_resp.status_code == 200

    # Login with correct credentials
    resp = client.post("/login/", data={  # use form data, not json!
        "username": "logintest@example.com",
        "password": "testpass"
    })
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_fail(client):
    # No user created for this login attempt
    resp = client.post("/login/", data={
        "username": "notexist@example.com",
        "password": "wrongpass"
    })
    assert resp.status_code == 400, resp.text
    data = resp.json()
    assert "Incorrect email or password" in data["detail"]
