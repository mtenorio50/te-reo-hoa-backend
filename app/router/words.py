from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud, models, ai_integration, auth
from app.database import get_db
from app.ai_integration import synthesize_maori_audio_with_polly
from app.utils import sanitize_level, sanitize_ai_data, extract_json_from_markdown, extract_ai_text
import os


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
        raise HTTPException(
            status_code=502, detail="AI did not return a usable response.")
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception:
        raise HTTPException(
            status_code=502, detail="Failed to parse AI response.")
    ai_data["level"] = sanitize_level(ai_data.get("level"))

    # Step 1: Create word without audio_url to get its ID
    db_word = crud.create_word(
        db, word.text, ai_data, ai_data["level"], audio_url=None)
    db.refresh(db_word)  # Get the generated id from DB

    # Step 2: Generate audio file named after db_word.id
    audio_url = None
    try:
        filename = await ai_integration.synthesize_maori_audio_with_polly(
            ai_data.get("translation", ""),
            # <--- Use word id as filename!
            filename_override=f"{db_word.id}.mp3"
        )
        audio_url = f"/static/audio/{filename}"
        # Step 3: Update db_word with the audio URL
        db_word.audio_url = audio_url
        db.commit()
        db.refresh(db_word)
    except Exception as e:
        # Audio generation failed, just proceed without audio
        pass

    return db_word  # Return the (possibly updated) DB object


@router.post("/words/{word_id}/generate_audio_polly", tags=["Words"])
async def generate_word_audio_polly(
    word_id: int,
    db: Session = Depends(auth.get_db),
    current_user=Depends(auth.require_admin)
):

    word = db.query(models.Word).filter_by(id=word_id).first()
    normalized = word.text.strip().lower()
    if crud.get_word_by_normalized(db, normalized):
        raise HTTPException(
            status_code=400, detail="Trabslation already exists")
    if not word:
        raise HTTPException(status_code=404, detail="Word not found.")
    maori_text = word.translation
    if not maori_text:
        raise HTTPException(
            status_code=400, detail="No translation available for this word.")
    try:
        filename = synthesize_maori_audio_with_polly(maori_text)
        word.audio_url = f"/static/audio/{filename}"
        db.commit()
        return {
            "audio_url": word.audio_url,
            "disclaimer": "Audio generated using Amazon Polly English voice. Māori pronunciation may not be accurate."
        }
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Polly audio generation failed: {e}")
