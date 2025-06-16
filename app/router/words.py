from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, ai_integration, auth
from app.database import get_db
from app.utils import sanitize_level, sanitize_ai_data, extract_json_from_markdown, extract_ai_text

router = APIRouter(tags=["Words"])

@router.get("/list", response_model=List[schemas.WordOut])
def list_words(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), current_user=Depends(auth.require_admin)):
    return crud.get_words(db, skip=skip, limit=limit)

@router.post("/add", response_model=schemas.WordOut)
async def add_word(
    word: schemas.WordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.require_admin)
):
    normalized = word.text.strip().lower()
    if crud.get_word_by_normalized(db, normalized):
        raise HTTPException(status_code=400, detail="Text already exists")
    result = await ai_integration.get_translation(word.text)
    raw_ai_text = extract_ai_text(result)
    if not raw_ai_text:
        raise HTTPException(status_code=502, detail="AI did not return a usable response.")
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception:
        raise HTTPException(status_code=502, detail="Failed to parse AI response.")
    ai_data["level"] = sanitize_level(ai_data.get("level"))
    return crud.create_word(db, word.text, ai_data, ai_data["level"])