from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.models import NewsItem
from app.schemas import NewsOut
from app.auth import require_admin, get_db
from app.ai_integration import get_positive_news_from_gemini

router = APIRouter()


async def refresh_news_in_db(db: Session, news_array):
    added = 0
    for item in news_array[:10]:  # Only up to 10
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
                published_date=datetime.utcnow(),  # use now or add from Gemini if available
                source_url=item.get("link"),
                source="",  # Gemini may not return; set if available
                image_urls=item.get("image_url", ""),
            )
            db.add(news)
            added += 1
        except Exception as e:
            print(f"Error saving news: {e}")
    db.commit()
    return added


@router.post("/refresh", tags=["Admin"])
async def admin_refresh_news(
    db: Session = Depends(get_db),
    current_user=Depends(require_admin)
):
    news_array = await get_positive_news_from_gemini()
    added = await refresh_news_in_db(db, news_array)
    return {"added": added, "message": f"{added} new news stories added."}


@router.get("/", response_model=List[NewsOut], tags=["News"])
def get_latest_news(db: Session = Depends(get_db)):
    return db.query(NewsItem).order_by(NewsItem.published_date.desc()).limit(15).all()
