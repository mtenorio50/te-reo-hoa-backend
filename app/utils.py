# app/utils.py
import json
import re
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from app.database import SessionLocal
from app.router.news import refresh_news_in_db
from app.ai_integration import get_positive_news_from_gemini
import asyncio

ALLOWED_LEVELS = ["beginner", "intermediate"]


def sanitize_level(ai_level: str) -> str:
    ai_level = (ai_level or "")
    if ai_level in ALLOWED_LEVELS:
        return ai_level
    return "beginner"  # Or prompt admin to choose


def extract_json_from_markdown(md_text: str) -> dict:
    """Extracts JSON object from markdown or plaintext AI response."""
    clean = re.sub(r"^```(?:json)?\s*", "",
                   md_text.strip(), flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean.strip())
    if not clean or not clean.strip().startswith("{"):
        print("AI response is not valid JSON:", repr(clean))
        raise ValueError("AI did not return valid JSON")
    return json.loads(clean)


def sanitize_ai_data(ai_data: dict) -> dict:
    """Ensures all expected keys exist and are non-None strings."""
    fields = ["translation", "type", "domain", "example", "notes"]
    for f in fields:
        ai_data[f] = str(ai_data.get(f) or "")
    return ai_data


def extract_ai_text(result: dict) -> str:
    """Safely extracts the AI response text from Gemini API result."""
    try:
        candidates = result.get("candidates")
        if not candidates or not isinstance(candidates, list):
            raise ValueError("No candidates in AI response")
        content = candidates[0].get("content")
        if not content or "parts" not in content or not content["parts"]:
            raise ValueError("No content parts in AI response")
        return content["parts"][0].get("text", "")
    except Exception as e:
        print("AI response extraction failed:", e)
        print("Full response:", result)
        return ""


def news_extract_json_from_markdown(md_text: str) -> str:
    """
    Strips markdown code fences (``` or ```json) from a string and returns the inner JSON string.
    """
    clean = re.sub(r"^```(?:json)?\s*", "",
                   md_text.strip(), flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean.strip())
    return clean


def scheduled_news_refresh():
    print("[SCHEDULER] Refreshing daily news...")
    db = SessionLocal()
    try:
        news_array = asyncio.run(get_positive_news_from_gemini())
        added = asyncio.run(refresh_news_in_db(db, news_array))
        print(f"[SCHEDULER] Added {added} new news stories.")
    except Exception as e:
        print(f"[SCHEDULER] News refresh failed: {e}")
    finally:
        db.close()


def start_scheduler():  # This scheduler will run 3am daily to get news automatically
    scheduler = BackgroundScheduler()
    scheduler.add_job(scheduled_news_refresh, CronTrigger(hour=3, minute=0))
    scheduler.start()
    print("[SCHEDULER] Started.")
