from enum import Enum
from typing import List, Optional, Dict, Any
from datetime import datetime

from pydantic import BaseModel, EmailStr, field_validator, ConfigDict

# ---------- User ----------


class UserCreate(BaseModel):
    """Schema for user registration input."""
    email: EmailStr
    password: str
    role: Optional[str] = "learner"


class UserOut(BaseModel):
    """Schema for user output (never includes password)."""
    id: int
    email: EmailStr
    role: str

    model_config = ConfigDict(from_attributes=True)


# ---------- Auth ----------


class Token(BaseModel):
    """JWT access token schema."""
    access_token: str
    token_type: str


# ---------- Word ----------


class WordBase(BaseModel):
    """Shared fields for words."""
    id: int
    text: str
    translation: Optional[str] = ""
    ipa: Optional[str] = ""
    phonetic: Optional[str] = ""
    level: Optional[str] = ""
    type: Optional[str] = ""
    domain: Optional[str] = ""
    example: Optional[str] = ""
    normalized: str
    notes: Optional[str] = ""

    model_config = ConfigDict(from_attributes=True)


class WordCreate(WordBase):
    """Input for adding a new word."""
    pass


class WordOut(WordBase):
    """Output for a word, with DB id."""
    id: int
    normalized: str

    model_config = ConfigDict(from_attributes=True)


class BatchWordCreate(BaseModel):
    texts: List[str]


class BatchWordResult(BaseModel):
    added: List[WordOut]
    skipped: List[str]

# ---------- Progress ----------


class ProgressStatusEnum(str, Enum):
    """Progress status enum."""
    unlearned = "unlearned"
    learned = "learned"
    review = "review"
    starred = "starred"


class WordProgressUpdate(BaseModel):
    """Input for updating progress on a word."""
    word_id: int
    status: ProgressStatusEnum


class WordProgressOut(BaseModel):
    """Output for a user's word progress entry."""
    word_id: int
    status: ProgressStatusEnum
    updated_at: Optional[str]


class UserProgressStats(BaseModel):
    """User's aggregate progress stats."""
    learned_count: int
    review_count: int
    starred_count: int
    unlearned_count: int
    total_words: int


class LearnedWord(BaseModel):
    """For showing learned words in a simple way."""
    word: str
    translation: str


# ---------- Quiz ----------


class QuizQuestion(BaseModel):
    """Schema for quiz question."""
    word_id: int
    question: str
    choices: List[str]  # E.g. ["whānau", "kai", "kura", "waka"]
    correct_index: int  # Index of correct answer in choices


class QuizAnswerSubmission(BaseModel):
    """Input for quiz answer submission."""
    word_id: int
    chosen_index: int
    
    


class QuizResult(BaseModel):
    """Result of quiz answer."""
    correct: bool
    


# ---------- News ----------


class NewsItem(BaseModel):
    """Single news item from external source (AI, web)."""
    title_english: str
    title_maori: Optional[str]
    summary_english: str
    summary_maori: Optional[str]
    published_date: str
    source_url: str
    source: str
    image_urls: List[str]
    created_at: str


class PositiveNewsResponse(BaseModel):
    """For batch return of positive news."""
    items: List[NewsItem]


class NewsOut(BaseModel):
    """News as stored in DB and returned from endpoints."""
    id: int
    title_english: str
    title_maori: Optional[str]
    summary_english: str
    summary_maori: Optional[str]
    published_date: str
    source_url: str
    source: str
    image_urls: List[str]
    created_at: str

    @field_validator('published_date', mode="before")
    def datetime_to_iso(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    @field_validator('created_at', mode="before")
    def created_at_to_iso(cls, v):
        if isinstance(v, datetime):
            return v.isoformat()
        return v

    @field_validator('image_urls', mode="before")
    def ensure_list(cls, v):
        if isinstance(v, str):
            # If DB stored as a string, convert to list with one item or try json.loads
            try:
                import json
                return json.loads(v)
            except Exception:
                return [v]
        if v is None:
            return []
        return v

    model_config = ConfigDict(from_attributes=True)


class BatchDeleteRequest(BaseModel):
    """IDs for batch deletion."""
    ids: list[int]

# ---------- Translation ----------


class TranslationRequest(BaseModel):
    """Input for translation endpoint."""
    text: str


class TranslationResponse(BaseModel):
    """Translation result."""
    translation: str


# ---------- TTS (Text-to-Speech) ----------

class TTSRequest(BaseModel):
    """Input for TTS generation."""
    text: str
    voice_id: Optional[str] = "Aria"  # AWS Polly voice ID
    output_format: Optional[str] = "mp3"

    @field_validator('text')
    @classmethod
    def validate_text(cls, v):
        if not v or not v.strip():
            raise ValueError('Text cannot be empty')
        if len(v.strip()) > 500:  # Reasonable limit for TTS
            raise ValueError('Text too long (max 500 characters)')
        return v.strip()


class TTSResponse(BaseModel):
    """Response for TTS generation."""
    audio_url: str
    text: str
    voice_id: str
    cached: bool = False
    message: Optional[str] = None
