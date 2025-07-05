from dotenv import load_dotenv
import json
import os
import itertools
import boto3
import httpx
import logging
import asyncio

logger = logging.getLogger(__name__)


load_dotenv()
timeout = httpx.Timeout(240.0, connect=10.0)
# Load and parse the keys from .env
GOOGLE_API_KEYS = [
    key.strip() for key in os.getenv("GOOGLE_AI_API_KEYS", "").split(",") if key.strip()
]

if not GOOGLE_API_KEYS:
    raise Exception("No Gemini API keys found in environment variables!")

# Create a round-robin iterator
key_cycle = itertools.cycle(GOOGLE_API_KEYS)


def get_next_api_key():
    return next(key_cycle)


AUDIO_DIR = "./static/audio/"
os.makedirs(AUDIO_DIR, exist_ok=True)
polly_client = boto3.client("polly", region_name="ap-southeast-2")


async def gemini_post(
    payload: dict,
    max_retries: int = 3,
    timeout=httpx.Timeout(240.0, connect=10.0),
    model: str = "gemini-2.5-flash"
):
    headers = {"Content-Type": "application/json"}
    for attempt in range(1, max_retries + 1):
        api_key = get_next_api_key()
        api_url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{model}:generateContent?key={api_key}"
        )
        try:
            async with httpx.AsyncClient(timeout=timeout) as client:
                resp = await client.post(api_url, headers=headers, json=payload)
                resp.raise_for_status()
                return resp.json()
        except httpx.ReadTimeout:
            logger.warning(
                f"Gemini API timed out on attempt {attempt}/{max_retries} using key {api_key[:5]}...{api_key[-3:]}"
            )
        except Exception as e:
            logger.error(
                f"Gemini API error on attempt {attempt} using key {api_key[:5]}...{api_key[-3:]}: {e}"
            )
        if attempt < max_retries:
            await asyncio.sleep(2 ** attempt)
    raise httpx.ReadTimeout(
        "Gemini API failed after several attempts (key rotation used)."
    )


async def get_translation(word: str, max_retries=3):
    headers = {"Content-Type": "application/json"}
    prompt = f"""
    Translate the following English word or phrase to Māori. For output, return ONLY a raw JSON object with these fields and nothing else:

    {{
    "translation": "...",   // just the translation no other else
    "ipa": "...",           // The correct IPA pronunciation for the Māori translation
    "phonetic": "..."       // A simple English phonetic spelling for the Māori translation
    "type": "...",          // e.g., noun, verb, etc.
    "domain": "...",        // e.g., greetings, number, weather, etc.
    "example": "...",       // Example usage in a sentence (in both Māori and English, if possible)
    "notes": "..."          // Cultural or usage notes (can be blank)
    }}

    If you do not know the answer for a field, use an empty string (""). Do NOT use markdown or any code fences—just output the JSON.

    Word or phrase: "{word}"
    """
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    headers = {"Content-Type": "application/json"}
    return await gemini_post(payload, max_retries=max_retries)


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
    try:
        result = await gemini_post(payload)
        # Extract the AI's response text (may include markdown code fences)
        raw_text = result["candidates"][0]["content"]["parts"][0]["text"]
        # Remove code fences if present
        if raw_text.startswith("```json"):
            raw_text = raw_text.replace("```json", "").strip()
        if raw_text.startswith("```"):
            raw_text = raw_text[3:].strip()
        if raw_text.endswith("```"):
            raw_text = raw_text[:-3].strip()
        return json.loads(raw_text)
    except Exception as e:
        logger.error("Failed to parse Gemini response: %s", e)
        logger.info("Raw response: %s", result)
        raise


async def synthesize_maori_audio_with_polly(
    maori_text, voice_id="Aria", output_format="mp3", filename_override=None
):
    response = polly_client.synthesize_speech(
        Text=maori_text, VoiceId=voice_id, OutputFormat=output_format, Engine="neural"
    )
    audio_stream = response.get("AudioStream")
    if not audio_stream:
        logger.error("No audio stream returned from Polly:", audio_stream)
        raise Exception("No audio stream returned from Polly.")
    filename = filename_override or f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
    audio_path = os.path.join(AUDIO_DIR, filename)
    with open(audio_path, "wb") as f:
        f.write(audio_stream.read())
    return filename


    # (Use same logic as your other Gemini calls, then parse as JSON)
    # Return as string or dict as you like (save in DB as needed)
    # See previous responses for example code
