import enum
from datetime import datetime

from sqlalchemy import (
    JSON,
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Text,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="learner")  # "admin" or "learner"
    created_at = Column(DateTime, default=datetime.utcnow)


class Word(Base):
    __tablename__ = "words"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, unique=True, index=True)
    translation = Column(String)
    ipa = Column(String)       # e.g., "ˈfaː.naʉ"
    phonetic = Column(String)  # e.g., "far-now" (simple English)
    level = Column(String)  # e.g., "Beginner", "Intermediate"
    type = Column(String)  # e.g., noun, verb, etc.
    domain = Column(String)  # e.g., greetings, food
    example = Column(Text)  # Example sentence
    # Lowercased version for dedup/search
    normalized = Column(String, index=True)
    notes = Column(Text)  # Cultural/usage notes


class ProgressStatus(enum.Enum):
    unlearned = "unlearned"
    learned = "learned"
    review = "review"
    starred = "starred"


class UserWordProgress(Base):
    __tablename__ = "user_word_progress"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    word_id = Column(Integer, ForeignKey("words.id"))
    status = Column(Enum(ProgressStatus), default=ProgressStatus.unlearned)
    updated_at = Column(DateTime, default=datetime.utcnow)


class NewsItem(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True, index=True)
    title_english = Column(String)
    title_maori = Column(String)
    summary_english = Column(String)
    summary_maori = Column(String)
    published_date = Column(DateTime)
    source_url = Column(String, unique=True)
    source = Column(String)
    image_urls = Column(JSON)
    created_at = Column(DateTime, default=datetime.utcnow)
    __table_args__ = (UniqueConstraint(
        "source_url", name="uq_news_source_url"),)
