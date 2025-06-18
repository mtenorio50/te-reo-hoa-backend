import httpx
import os
import boto3
from .utils import extract_json_from_markdown, sanitize_ai_data
from dotenv import load_dotenv
from app.schemas import NewsItem


load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"


AUDIO_DIR = "./static/audio/"
os.makedirs(AUDIO_DIR, exist_ok=True)
polly_client = boto3.client("polly", region_name="ap-southeast-2")


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


async def synthesize_maori_audio_with_polly(maori_text, voice_id="Aria", output_format="mp3"):
    response = polly_client.synthesize_speech(
        Text=maori_text,
        VoiceId=voice_id,
        OutputFormat=output_format,
        Engine="neural"
    )
    audio_stream = response.get("AudioStream")
    if not audio_stream:
        raise Exception("No audio stream returned from Polly.")
    filename = f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, filename)
    with open(audio_path, "wb") as f:
        f.write(audio_stream.read())
    return filename


async def get_pronunciation_guide(maori_word):
    prompt = f"""For the Māori word "{maori_word}", provide:
- The correct IPA pronunciation guide (International Phonetic Alphabet)
- A simple English phonetic spelling
Return your answer as a valid JSON object, no markdown, like:
{{
  "ipa": "...",
  "phonetic": "..."
}}
"""
    # (Use same logic as your other Gemini calls, then parse as JSON)
    # Return as string or dict as you like (save in DB as needed)
    # See previous responses for example code
