import httpx
import os
from .utils import extract_json_from_markdown, sanitize_ai_data
from dotenv import load_dotenv
from app.schemas import NewsItem


load_dotenv()

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


async def get_positive_news_from_gemini(news_items: list[NewsItem]) -> list[dict]:
    prompt = (
        
        
        "FOCUS ON POSITIVE NEWS ONLY: Select only positive, uplifting, and constructive news "
        "stories. Avoid negative news such as conflicts, tragedies, controversies, or problems. "
        "Focus on achievements, celebrations, cultural events, educational initiatives, business "
        "successes, and community developments.\n\n"
        "Given the following news articles, return a JSON array of up to 15 POSITIVE news items. "
        "Each item should have 'title' and 'content'. Output ONLY the JSON array, no markdown or explanation.\n\n"
        "Each item should have 'title' and 'content'.\n\n"
        f"{[item.dict() for item in news_items]}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient() as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        # The Gemini API response will have the text in a nested structure
        response_json = resp.json()
        try:
            raw_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            import json
            return json.loads(raw_text)
        except Exception as e:
            print("Failed to parse Gemini response:", e)
            print("Raw response:", response_json)
            raise
