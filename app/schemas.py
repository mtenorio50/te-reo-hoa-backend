from pydantic import BaseModel, EmailStr
from typing import Optional


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


class WordCreate(BaseModel):
    text: str


class WordBase(BaseModel):
    id: int
    text: str
    translation: Optional[str] = ""
    level: Optional[str] = ""
    type: Optional[str] = ""
    domain: Optional[str] = ""
    example: Optional[str] = ""
    audio_url: Optional[str] = None
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
    translation: Optional[str] = ""
    type: Optional[str] = ""
    domain: Optional[str] = ""
    example: Optional[str] = ""
    audio_url: Optional[str] = None
    normalized: str
    notes: Optional[str] = ""

    class Config:
        from_attributes = True


class WordCreate(BaseModel):
    text: str


class TranslationRequest(BaseModel):
    text: str


class TranslationResponse(BaseModel):
    translation: str
