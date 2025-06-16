from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app import schemas, crud, models, auth
from app.database import get_db
from typing import List

router = APIRouter(tags=["Progress"])


@router.post("/word", response_model=schemas.WordProgressOut)
def mark_word_progress(
    progress: schemas.WordProgressUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    word = db.query(models.Word).filter_by(id=progress.word_id).first()
    if not word:
        raise HTTPException(status_code=404, detail="Word does not exist.")
    entry = crud.set_word_progress(
        db, current_user.id, progress.word_id, progress.status.value
    )
    return schemas.WordProgressOut(
        word_id=entry.word_id,
        status=entry.status,
        updated_at=entry.updated_at.isoformat() if entry.updated_at else None,
    )


@router.get("/stats", response_model=schemas.UserProgressStats)
def get_progress_stats(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    stats = crud.get_user_progress_stats(db, current_user.id)
    return schemas.UserProgressStats(**stats)


@router.get("/learned_words", response_model=List[schemas.LearnedWord])
def get_learned_words(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user)
):
    words = crud.get_learned_words_for_user(db, current_user.id)
    return words
