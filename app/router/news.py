from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.ai_integration import get_positive_news_from_gemini
from app.auth import get_db, require_admin
from app.models import NewsItem
from app.schemas import NewsOut, BatchDeleteRequest

import logging
logger = logging.getLogger(__name__)

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
            logger.error(f"Error saving news: {e}")
    db.commit()
    return added


@router.get("/", response_model=List[NewsOut], tags=["News"],
            summary="Get latest news",
            description="Returns the latest 10 positive news stories.")
def get_latest_news(db: Session = Depends(get_db), current_user=Depends(require_admin)):
    """List the 10 most recent news items."""
    return db.query(NewsItem).order_by(NewsItem.published_date.desc()).limit(10).all()


@router.get("/all", response_model=List[NewsOut], tags=["News"],
            summary="List all news",
            description="Returns a paginated list of all news stories. Admin access required.")
def list_all_news(
    db: Session = Depends(get_db),
    page: int = 1,
    limit: int = 10,
    current_user=Depends(require_admin),
):
    """List all news stories with pagination (admin only).
     page=1 returns first 10, page=2 returns next 10, etc."""
    offset = (page - 1) * limit
    news_items = (
        db.query(NewsItem)
        .order_by(NewsItem.published_date.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    # Ensure returned objects are converted for Pydantic schema
    return [NewsOut.from_orm(item) for item in news_items]


@router.post("/refresh", tags=["News"], summary="Refresh news from AI",
             description="Fetches new positive news stories using Gemini AI and saves them to the database. Admin access required.")
async def admin_refresh_news(
    db: Session = Depends(get_db), current_user=Depends(require_admin)
):
    """Trigger a news refresh from Gemini AI (admin only)."""
    news_array = await get_positive_news_from_gemini()
    added = await refresh_news_in_db(db, news_array)
    return {"added": added, "message": f"{added} new news stories added."}


@router.delete("/{news_id}", tags=["News"],
               summary="Delete a news item",
               description="Deletes a news story by its ID. Admin access required.")
def delete_news(
    news_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    """Delete a news item by ID (admin only)."""
    news = db.query(NewsItem).filter_by(id=news_id).first()
    if not news:
        raise HTTPException(status_code=404, detail="News item not found")
    db.delete(news)
    db.commit()
    return {"message": f"News item {news_id} deleted"}


"""
@router.delete("/batch", tags=["News"])
def batch_delete_news(
    request: BatchDeleteRequest,
    db: Session = Depends(get_db),
    current_user=Depends(require_admin),
):
    deleted = 0
    for news_id in request.ids:
        news = db.query(NewsItem).filter_by(id=news_id).first()
        if news:
            db.delete(news)
            deleted += 1
    db.commit()
    return {"deleted": deleted, "message": f"{deleted} news items deleted"}
"""
