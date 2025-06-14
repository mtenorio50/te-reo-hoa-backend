import httpx
import os
from .utils import extract_json_from_markdown, sanitize_ai_data

GOOGLE_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"


async def get_translation(word: str):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    Translate the following English word or phrase to Māori. For output, return ONLY a raw JSON object with these fields and nothing else:

    {{
    "translation": "...",
    "type": "...",          // e.g., noun, verb, etc.
    "domain": "...",        // e.g., greetings, number, weather, etc.
    "example": "...",       // Example usage in a sentence (in both Māori and English, if possible)
    "notes": "..."          // Cultural or usage notes (can be blank)
    }}

    If you do not know the answer for a field, use an empty string (""). Do NOT use markdown or any code fences—just output the JSON.

    Word or phrase: "{word}"
    """
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        return resp.json()
