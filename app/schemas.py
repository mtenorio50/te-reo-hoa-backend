from pydantic import BaseModel, EmailStr
from typing import Optional, List
from enum import Enum


class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "learner"


class UserOut(BaseModel):
    id: int
    email: EmailStr
    role: str

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class WordBase(BaseModel):
    id: int
    text: str
    translation: Optional[str] = ""
    level: Optional[str] = ""
    type: Optional[str] = ""
    domain: Optional[str] = ""
    example: Optional[str] = ""
    audio_url: Optional[str] = ""
    normalized: str
    notes: Optional[str] = ""

    class Config:
        from_attributes = True


class WordCreate(WordBase):
    pass


class WordOut(WordBase):
    id: int
    normalized: str

    class Config:
        from_attributes = True


class WordOut(BaseModel):
    id: int
    text: str
    level: str
    translation: Optional[str] = ""
    type: Optional[str] = ""
    domain: Optional[str] = ""
    example: Optional[str] = ""
    audio_url: Optional[str] = ""
    normalized: str
    notes: Optional[str] = ""

    class Config:
        from_attributes = True


class LevelEnum(str, Enum):
    beginner = "Basic"
    intermediate = "Intermediate"


class WordCreate(BaseModel):
    text: str


class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    translation: str


class ProgressStatusEnum(str, Enum):
    unlearned = "unlearned"
    learned = "learned"
    review = "review"
    starred = "starred"


class WordProgressUpdate(BaseModel):
    word_id: int
    status: ProgressStatusEnum


class WordProgressOut(BaseModel):
    word_id: int
    status: ProgressStatusEnum
    updated_at: Optional[str]


class UserProgressStats(BaseModel):
    learned_count: int
    review_count: int
    starred_count: int
    unlearned_count: int
    total_words: int


class LearnedWord(BaseModel):
    word: str
    translation: str


class QuizQuestion(BaseModel):
    word_id: int
    question: str
    choices: List[str]        # E.g. ["whānau", "kai", "kura", "waka"]
    correct_index: int        # Index of correct answer in choices


class QuizAnswerSubmission(BaseModel):
    word_id: int
    chosen_index: int


class QuizResult(BaseModel):
    correct: bool
    correct_answer: str


class NewsItem(BaseModel):
    title: str
    content: str
    link: str


class PositiveNewsResponse(BaseModel):
    items: List[NewsItem]
