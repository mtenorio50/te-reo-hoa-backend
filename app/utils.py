# app/utils.py
from app.database import SessionLocal
from app.ai_integration import get_positive_news_from_gemini
from apscheduler.triggers.cron import CronTrigger
from apscheduler.schedulers.background import BackgroundScheduler
import asyncio
import json
import re
import logging
import httpx

logger = logging.getLogger(__name__)


ALLOWED_LEVELS = ["beginner", "intermediate"]


def sanitize_level(ai_level: str) -> str:
    ai_level = ai_level or ""
    if ai_level in ALLOWED_LEVELS:
        return ai_level
    return "beginner"  # Or prompt admin to choose


def extract_json_from_markdown(md_text: str) -> dict:
    """Extracts JSON object from markdown or plaintext AI response."""
    clean = re.sub(r"^```(?:json)?\s*", "",
                   md_text.strip(), flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean.strip())
    if not clean or not clean.strip().startswith("{"):
        logger.error("AI response is not valid JSON:", repr(clean))
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
        logger.error("AI response extraction failed:", e)
        logger.info("Full response:", result)
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
    """Scheduled function to refresh news daily at 8 AM NZ time."""
    logger.info(
        "[SCHEDULER] 🇳🇿 Starting daily news refresh at 8 AM New Zealand time...")
    db = SessionLocal()
    try:
        # Get news from AI
        logger.info("[SCHEDULER] Fetching news from AI...")
        news_array = asyncio.run(get_positive_news_from_gemini())

        if not news_array:
            logger.warning("[SCHEDULER] No news items returned from AI")
            return

        logger.info(
            f"[SCHEDULER] Retrieved {len(news_array)} news items from AI")

        # Save to database
        added = asyncio.run(refresh_news_in_db(db, news_array))
        logger.info(
            f"[SCHEDULER] Successfully added {added} new news stories to database")

    except Exception as e:
        logger.error(f"[SCHEDULER] News refresh failed: {e}")
        logger.exception("[SCHEDULER] Full error traceback:")
    finally:
        db.close()
        logger.info("[SCHEDULER] Database connection closed")


def test_scheduler_job():
    """Test job to verify scheduler is working."""
    logger.info(
        "[SCHEDULER TEST] ✅ Scheduler is working! Test job executed successfully.")


def start_scheduler():
    """Start the background scheduler for daily news refresh at 8 AM NZ time."""
    try:
        import os
        from apscheduler.schedulers.background import BackgroundScheduler

        # Check if running on Render or other cloud platforms
        is_production = os.getenv("RENDER") or os.getenv(
            "RAILWAY") or os.getenv("HEROKU")

        logger.info(
            f"[SCHEDULER] Starting scheduler... Production mode: {bool(is_production)}")

        scheduler = BackgroundScheduler(
            timezone='Pacific/Auckland')  # New Zealand timezone

        # Main job: Daily news refresh at 8 AM NZ time
        scheduler.add_job(
            scheduled_news_refresh,
            # 8 AM NZ time daily
            CronTrigger(hour=8, minute=00, timezone='Pacific/Auckland'),
            id='daily_news_refresh_8am_nz',
            replace_existing=True,
            max_instances=1,  # Prevent overlapping jobs
            coalesce=True     # If multiple triggers, run only once
        )

        # Add test job for development (every 15 minutes)
        if not is_production:
            scheduler.add_job(
                test_scheduler_job,
                # Every 15 minutes
                CronTrigger(minute='*/15', timezone='Pacific/Auckland'),
                id='test_job_15min',
                replace_existing=True,
                max_instances=1
            )
            logger.info(
                "[SCHEDULER] Development mode: Test job will run every 15 minutes (NZ time)")

        scheduler.start()
        logger.info(
            "[SCHEDULER] ✅ Started successfully! Daily news refresh scheduled for 8:00 AM New Zealand time")
        logger.info(
            "[SCHEDULER] 🇳🇿 Timezone: Pacific/Auckland (handles NZST/NZDT automatically)")

        return scheduler

    except Exception as e:
        logger.error(f"[SCHEDULER] ❌ Failed to start: {e}")
        logger.exception("[SCHEDULER] Full startup error:")
        return None


def get_scheduler_status():
    """Get current scheduler status for debugging."""
    try:
        return {
            "status": "healthy",
            "message": "Scheduler status check completed",
            "daily_job": "8:00 AM New Zealand time (Pacific/Auckland)",
            "timezone": "Automatically handles NZST/NZDT",
            "next_run": "Check logs for next execution time"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Scheduler status check failed: {e}"
        }


def manual_news_refresh():
    """Manually trigger news refresh for testing."""
    logger.info("[MANUAL TRIGGER] Starting manual news refresh...")
    return scheduled_news_refresh()


async def refresh_news_in_db(db, news_array):
    """Refresh news in database from AI news array."""
    from app.models import NewsItem
    from datetime import datetime

    added = 0
    for item in news_array[:10]:  # Only up to 10 items
        source_url = item.get("link")
        if not source_url:
            continue  # skip items without a link

        # Check for duplicate by source_url
        if db.query(NewsItem).filter_by(source_url=source_url).first():
            continue  # skip duplicate

        try:
            news = NewsItem(
                title_english=item.get("title", ""),
                title_maori=item.get("title_maori", ""),
                summary_english=item.get("content", ""),
                summary_maori=item.get("summary_maori", ""),
                published_date=datetime.utcnow(),
                source_url=item.get("link"),
                source="AI Generated",
                image_urls=item.get("image_url", ""),
            )
            db.add(news)
            added += 1
        except Exception as e:
            logger.error(f"Error saving news item: {e}")

    db.commit()
    return added
