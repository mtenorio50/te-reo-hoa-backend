import httpx
import os
import json
import boto3
# from app.utils import extract_json_from_markdown, sanitize_ai_data
from dotenv import load_dotenv
# from app.schemas import NewsItem


load_dotenv()
timeout = httpx.Timeout(120.0, connect=10.0)

GOOGLE_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
GEMINI_MODEL = "gemini-2.5-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GOOGLE_API_KEY}"


AUDIO_DIR = "./static/audio/"
os.makedirs(AUDIO_DIR, exist_ok=True)
polly_client = boto3.client("polly", region_name="ap-southeast-2")


async def get_translation(word: str):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    Translate the following English word or phrase to Māori. For output, return ONLY a raw JSON object with these fields and nothing else:

    {{
    "translation": "...",   // just the translation no other else
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


async def get_positive_news_from_gemini():
    prompt = (
        "FOCUS ON POSITIVE NEWS ONLY: Select only positive, uplifting, and constructive news "
        "stories. Avoid negative news such as conflicts, tragedies, controversies, or problems. "
        "Focus on achievements, celebrations, cultural events, educational initiatives, business "
        "successes, and community developments.\n\n"
        "Use live web search to find recent news from NZ sources. "
        "Translate title and summary to maori, name it title_maori and summary_maori"
        "if there is thumbnail or image available include it and store the link and name it image_url"
        "Return a JSON array of up to 10 POSITIVE news items. Each should have 'title' and 'content' and 'link'. "
        "Output ONLY the JSON array, no markdown or explanation.\n\n"
    )
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=timeout) as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        response_json = resp.json()
        try:
            raw_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            if raw_text.startswith("```json"):
                raw_text = raw_text.replace("```json", "").strip()
            if raw_text.startswith("```"):
                raw_text = raw_text[3:].strip()
            if raw_text.endswith("```"):
                raw_text = raw_text[:-3].strip()
            return json.loads(raw_text)
        except Exception as e:
            print("Failed to parse Gemini response:", e)
            print("Raw response:", response_json)
            raise


async def synthesize_maori_audio_with_polly(maori_text, voice_id="Aria", output_format="mp3", filename_override=None):
    response = polly_client.synthesize_speech(
        Text=maori_text,
        VoiceId=voice_id,
        OutputFormat=output_format,
        Engine="neural"
    )
    audio_stream = response.get("AudioStream")
    if not audio_stream:
        raise Exception("No audio stream returned from Polly.")
    filename = filename_override or f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
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
