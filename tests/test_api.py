import os

import httpx

api_key = os.getenv("GOOGLE_AI_API_KEY")
url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
payload = {
    "contents": [{"role": "user", "parts": [{"text": "Translate 'family' to Māori."}]}]
}

response = httpx.post(url, json=payload, timeout=20)
print(response.status_code)
print(response.text)
