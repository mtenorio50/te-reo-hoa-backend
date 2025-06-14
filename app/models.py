from sqlalchemy import Column, Integer, String, DateTime, Text
from .database import Base
from datetime import datetime


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
    level = Column(String)                # e.g., "Beginner", "Intermediate"
    type = Column(String)                 # e.g., noun, verb, etc.
    domain = Column(String)               # e.g., greetings, food
    example = Column(Text)                # Example sentence
    audio_url = Column(String)            # URL for audio pronunciation
    # Lowercased version for dedup/search
    normalized = Column(String, index=True)
    notes = Column(Text)                  # Cultural/usage notes
