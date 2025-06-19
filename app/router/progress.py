from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import auth, crud, models, schemas
from app.database import get_db

import logging

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Progress"])


@router.post("/word", response_model=schemas.WordProgressOut,
             summary="Update word progress",
             description="Marks a word as learned, reviewed, starred, or unlearned for the current user.")
def mark_word_progress(
    progress: schemas.WordProgressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """Update user progress status for a word."""
    word = db.query(models.Word).filter_by(id=progress.word_id).first()
    if not word:
        logger.error("Word does not exist: %s", word)
        raise HTTPException(status_code=404, detail="Word does not exist.")
    entry = crud.set_word_progress(
        db, current_user.id, progress.word_id, progress.status.value
    )
    return schemas.WordProgressOut(
        word_id=entry.word_id,
        status=entry.status,
        updated_at=entry.updated_at.isoformat() if entry.updated_at else None,
    )


@router.get("/stats", response_model=schemas.UserProgressStats,
            summary="Get user progress stats",
            description="Retrieves aggregate learning statistics for the current user.")
def get_progress_stats(
    db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)
):
    """Get progress statistics for the user."""
    stats = crud.get_user_progress_stats(db, current_user.id)
    return schemas.UserProgressStats(**stats)


@router.get("/learned_words", response_model=List[schemas.LearnedWord],
            summary="List learned words",
            description="Returns a list of all words marked as 'learned' by the current user.")
def get_learned_words(
    db: Session = Depends(get_db), current_user=Depends(auth.get_current_user)
):
    """List all words the user has learned."""
    words = crud.get_learned_words_for_user(db, current_user.id)
    return words
