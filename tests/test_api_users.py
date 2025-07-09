

def test_admin_can_list_users(client, register_and_login_admin):
    token = register_and_login_admin
    resp = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    users = resp.json()
    assert isinstance(users, list)

def test_learner_cannot_list_users(client, register_and_login_learner):
    token = register_and_login_learner
    resp = client.get("/users/", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 403

def test_unauthenticated_cannot_list_users(client):
    resp = client.get("/users/")
    assert resp.status_code == 401
