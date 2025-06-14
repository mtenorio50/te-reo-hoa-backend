from sqlalchemy.orm import Session
from . import models, schemas


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


def create_word(db: Session, text: str, ai_data: dict):
    normalized = text.strip().lower()
    db_word = models.Word(
        text=text.strip(),
        translation=ai_data.get("translation"),
        level=ai_data.get("level"),
        type=ai_data.get("type"),
        domain=ai_data.get("domain"),
        example=ai_data.get("example"),
        audio_url=None,  # to be added later
        normalized=normalized,
        notes=ai_data.get("notes"),
    )
    db.add(db_word)
    db.commit()
    db.refresh(db_word)
    return db_word


def get_users(db: Session):
    return db.query(models.User).all()
