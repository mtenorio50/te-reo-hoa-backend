# endpoint test, will use "list all users" endpoint

def test_list_users_requires_admin(client):
    # Register and login as a normal (non-admin) user
    reg = client.post("/users/register", json={
        "email": "normaluser@example.com",
        "password": "test"
    })
    assert reg.status_code == 200

    login = client.post("/login/", data={
        "username": "normaluser@example.com",
        "password": "test"
    })
    token = login.json()["access_token"]

    # Try to access protected endpoint
    resp = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert resp.status_code == 403  # Forbidden (not admin)


def test_list_users_unauthenticated(client):
    # Try to access protected endpoint without any token
    resp = client.get("/users/")
    assert resp.status_code == 401  # Unauthorized


def test_list_users_as_admin(client, db_session):
    # 1. Register a normal user (to have someone in the list)
    client.post("/users/register", json={
        "email": "someone@example.com",
        "password": "secret"
    })

    # 2. Register an admin candidate
    reg = client.post("/users/register", json={
        "email": "adminuser@example.com",
        "password": "adminpass"
    })
    user_id = reg.json()["id"]

    # 3. Login as the admin candidate (still not admin yet)
    login = client.post("/login/", data={
        "username": "adminuser@example.com",
        "password": "adminpass"
    })
    token = login.json()["access_token"]

    # 4. Promote this user to admin (simulate as admin by overriding dependency or direct DB update)
    # We'll use the API: /users/{user_id}/set_admin, but this also needs admin!
    # So let's promote in the DB directly for test purposes:
   
    from app.models import User
    user = db_session.query(User).filter_by(email="adminuser@example.com").first()
    assert user is not None  # helpful assertion for debugging
    user.role = "admin"
    db_session.commit()

    # 5. Now, login again (to get updated role in token)
    login2 = client.post("/login/", data={
        "username": "adminuser@example.com",
        "password": "adminpass"
    })
    admin_token = login2.json()["access_token"]

    # 6. Now, access the protected endpoint
    resp = client.get(
        "/users/",
        headers={"Authorization": f"Bearer {admin_token}"}
    )
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)
    assert any(u["email"] == "adminuser@example.com" for u in users)
