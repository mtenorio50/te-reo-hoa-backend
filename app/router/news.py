import os
import httpx
import feedparser
from fastapi import APIRouter, HTTPException
from typing import List
from app.schemas import NewsItem, PositiveNewsResponse
from app.utils import news_extract_json_from_markdown
import json

# Gemini API setup
GOOGLE_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GOOGLE_API_KEY}"

RSS_FEEDS = [
    "https://www.teaomaori.news/rss.xml",
    "https://www.teaonews.co.nz/rss.xml",
    "https://www.rnz.co.nz/rss/kawe-korero.xml"
]

router = APIRouter(prefix="/news", tags=["News"])

async def fetch_news() -> List[NewsItem]:
    news_items = []
    async with httpx.AsyncClient(timeout=20.0) as client:
        for url in RSS_FEEDS:
            try:
                resp = await client.get(url)
                resp.raise_for_status()
                feed = feedparser.parse(resp.text)
                for entry in feed.entries:
                    news_items.append(
                        NewsItem(
                            title=entry.title,
                            content=getattr(entry, "summary", "") or getattr(entry, "description", ""),
                            link=entry.link
                        )
                    )
            except Exception as e:
                print(f"Error fetching {url}: {e}")
    return news_items

async def get_positive_news_from_gemini(news_items: List[NewsItem], limit: int = 15) -> List[NewsItem]:
    prompt = (
        "Given the following news articles, return a JSON array of up to 15 POSITIVE news items. "
        "Each item should have 'title', 'content' and 'link' (the original article URL). Only include news that is positive, uplifting, or hopeful. "
        "Output ONLY the JSON array, no markdown or explanation.\n\n"
        f"{[item.dict() for item in news_items]}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        response_json = resp.json()
        try:
            raw_text = response_json["candidates"][0]["content"]["parts"][0]["text"]
            clean_json = news_extract_json_from_markdown(raw_text)
            items = json.loads(clean_json)
            # Ensure we return NewsItem objects and limit to 15
            return [NewsItem(**item) for item in items][:limit]
        except Exception as e:
            print("Failed to parse Gemini response:", e)
            print("Raw response:", response_json)
            raise HTTPException(status_code=502, detail="Failed to parse Gemini AI response.")

@router.get("/", response_model=PositiveNewsResponse)
async def get_positive_news():
    news_items = await fetch_news()
    if not news_items:
        raise HTTPException(status_code=404, detail="No news found.")
    try:
        positive_news = await get_positive_news_from_gemini(news_items, limit=15)
    except Exception as e:
        print("Gemini AI error:", e)
        raise HTTPException(status_code=502, detail="Error with Gemini AI.")
    return PositiveNewsResponse(items=positive_news)