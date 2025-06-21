from datetime import datetime, date
from sqlalchemy.orm import Session
from app import models, schemas

import random

_word_of_day_cache = {"date": None, "word": None}


def create_user(db: Session, user: schemas.UserCreate, hashed_pw: str):
    db_user = models.User(
        email=user.email,
        hashed_password=hashed_pw,
        role=user.role,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def set_user_role(db: Session, user_id: int, role: str):
    user = db.query(models.User).get(user_id)
    if user:
        user.role = role
        db.commit()
        db.refresh(user)
    return user


def get_word_by_normalized(db: Session, normalized: str):
    return db.query(models.Word).filter(models.Word.normalized == normalized).first()


def create_word(db: Session, text: str, ai_data: dict, level, audio_url=None):
    normalized = text.strip().lower()
    db_word = models.Word(
        text=text.strip(),
        translation=ai_data.get("translation"),
        level=level.strip(),
        type=ai_data.get("type"),
        domain=ai_data.get("domain"),
        example=ai_data.get("example"),
        audio_url=audio_url,
        normalized=normalized,
        notes=ai_data.get("notes"),
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def get_users(db: Session):
    return db.query(models.User).all()


def get_words(db: Session, offset: int = 0, limit: int = 10):
    return (
        db.query(models.Word)
        .order_by(models.Word.text.asc())   # Sort alphabetically
        .offset(offset)
        .limit(limit)
        .all()
    )


def set_word_progress(db: Session, user_id: int, word_id: int, status: str):
    entry = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, word_id=word_id)
        .first()
    )
    if entry:
        entry.status = status
        entry.updated_at = datetime.utcnow()
    else:
        entry = models.UserWordProgress(
            user_id=user_id, word_id=word_id, status=status)
        db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry


def get_user_progress_stats(db: Session, user_id: int):
    total_words = db.query(models.Word).count()
    learned = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, status="learned")
        .count()
    )
    review = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, status="review")
        .count()
    )
    starred = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, status="starred")
        .count()
    )
    unlearned = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, status="unlearned")
        .count()
    )
    return {
        "learned_count": learned,
        "review_count": review,
        "starred_count": starred,
        "unlearned_count": unlearned,
        "total_words": total_words,
    }


def get_learned_words_for_user(db: Session, user_id: int):
    learned_progress = (
        db.query(models.UserWordProgress)
        .filter_by(user_id=user_id, status="learned")
        .all()
    )
    word_ids = [progress.word_id for progress in learned_progress]
    # Just return the text of each word
    words = db.query(models.Word).filter(models.Word.id.in_(word_ids)).all()
    # Return word text and translation as a list of dicts
    return [{"word": word.text, "translation": word.translation} for word in words]


def filter_words(db: Session, search_by: str, value: str, offset: int = 0, limit: int = 10):
    q = db.query(models.Word)
    if search_by == "word":
        q = q.filter(models.Word.text.ilike(f"%{value}%"))
    elif search_by == "level" and value.lower() in ["beginner", "intermediate"]:
        q = q.filter(models.Word.level.ilike(value))
    else:
        return []  # Return empty if search_by or value not supported
    return q.order_by(models.Word.text.asc()).offset(offset).limit(limit).all()


def get_word_of_the_day(db: Session):
    today = date.today()
    if _word_of_day_cache["date"] == today and _word_of_day_cache["word"]:
        return _word_of_day_cache["word"]
    words = db.query(models.Word).all()
    if not words:
        return None
    word = random.choice(words)
    _word_of_day_cache["date"] = today
    _word_of_day_cache["word"] = word
    return word
