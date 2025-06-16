import httpx
import os
import json
from fastapi import APIRouter, HTTPException

router = APIRouter()

GOOGLE_AI_API_KEY = os.getenv("GOOGLE_AI_API_KEY")
GEMINI_MODEL = "gemini-2.0-flash"
API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent?key={GOOGLE_AI_API_KEY}"

PROMPT = """
IMPORTANT: Use real-time web search to find the latest news articles about Māori culture, people, language (Te Reo Māori), and related topics from New Zealand. DO NOT use your training data or existing knowledge base. You MUST search the internet for current, up-to-date news articles.

SEARCH REQUIREMENT: Perform live web searches on news websites to find recent articles. Access current news from real websites, not from your pre-existing knowledge.

IMPORTANT: You MUST return ONLY valid JSON. DO NOT use markdown code blocks (```json or ```). DO NOT add any explanatory text before or after the JSON. Return raw JSON only.

TIME REQUIREMENT: Only return news articles published within the last 30 days (1 month). Do not include any news older than 1 month. Ensure all articles are recent and current by searching live news sources.

FOCUS ON POSITIVE NEWS ONLY: Select only positive, uplifting, and constructive news stories. Avoid negative news such as conflicts, tragedies, controversies, or problems. Focus on achievements, celebrations, cultural events, educational initiatives, business successes, and community developments.

JSON structure:
{
  "news": [
    {
      "title": {
        "english": "News article title in English",
        "maori": "News article title translated to Te Reo Māori"
      },
      "summary": {
        "english": "Brief summary of the news article in English",
        "maori": "Brief summary translated to Te Reo Māori"
      },
      "publishedDate": "Publication date in ISO format or relative time",
      "sourceUrl": "Direct link to the original news article",
      "source": "Name of the news source/publication",
      "imageUrls": ["array of image URLs if available, empty array if none"]
    }
  ]
}

Requirements:
- USE REAL-TIME WEB SEARCH - do not rely on training data
- Search live news websites for current articles
- Return 10 recent POSITIVE news articles only
- ALL articles must be published within the last 30 days (1 month)
- Focus on NZ sources: NZ Herald, Stuff, RNZ, Māori Television
- Verify all URLs are real and accessible
- Select uplifting stories about: cultural celebrations, educational success, business achievements, community initiatives, language revitalization, arts and culture, positive social developments
- Avoid negative topics: conflicts, tragedies, controversies, legal disputes, health crises
- Ensure valid JSON syntax (no trailing commas)
- NO markdown formatting, NO code blocks, NO explanatory text
- Start response with { and end with }
"""


async def get_gemini_positive_news():
    payload = {
        "contents": [
            {
                "parts": [
                    {"text": PROMPT}
                ]
            }
        ]
    }
    headers = {"Content-Type": "application/json"}
    async with httpx.AsyncClient(timeout=60.0) as client:
        resp = await client.post(API_URL, json=payload, headers=headers)
        resp.raise_for_status()
        result = resp.json()
    # Extract only the raw JSON from Gemini output
    text = result["candidates"][0]["content"]["parts"][0]["text"]
    try:
        # Defensive: Gemini may occasionally add code blocks (rare, but handle just in case)
        if text.startswith("```json"):
            text = text.replace("```json", "").strip()
        if text.startswith("```"):
            text = text[3:].strip()
        if text.endswith("```"):
            text = text[:-3].strip()
        news_json = json.loads(text)
        # Validate top-level keys
        if "news" not in news_json or not isinstance(news_json["news"], list):
            raise ValueError("Invalid JSON structure from Gemini")
        return news_json
    except Exception as e:
        print("Gemini raw output:", text)
        print("Parsing error:", e)
        raise HTTPException(
            status_code=502, detail="Failed to parse Gemini's news JSON.")


@router.get("/", tags=["News"])
async def get_positive_news():
    try:
        news_json = await get_gemini_positive_news()
    except Exception as e:
        raise HTTPException(
            status_code=502, detail=f"Error getting news: {str(e)}")
    return news_json
