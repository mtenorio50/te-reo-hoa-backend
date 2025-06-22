import requests

BASE_URL = "http://localhost:8000"

# Register a user
resp = requests.post(f"{BASE_URL}/users/register", json={
    "email": "testing@chatgpt.com",
    "password": "StrongPass123"
})
print(resp.json())

# Login
resp = requests.post(f"{BASE_URL}/login", data={
    "username": "testing@chatgpt.com",
    "password": "StrongPass123"
})
print(resp.json())
