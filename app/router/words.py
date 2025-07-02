from app.utils import (
    extract_ai_text,
    extract_json_from_markdown,
    sanitize_ai_data,
    sanitize_level,
)
from app.database import get_db
from app.ai_integration import synthesize_maori_audio_with_polly
from app import ai_integration, auth, crud, models, schemas
from sqlalchemy.orm import Session
from fastapi import APIRouter, Depends, HTTPException, Body
from typing import List
import os
import logging

logger = logging.getLogger(__name__)


router = APIRouter(tags=["Words"])


@router.get("/list", response_model=List[schemas.WordOut],
            summary="List words",
            description="Returns a paginated list of all words in the dictionary. Admin access required.")
def list_words(
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """List all dictionary words (paginated, all authenticated users)."""
    offset = (page - 1) * limit
    return crud.get_words(db, offset=offset, limit=limit)


@router.get("/search", response_model=List[schemas.WordOut],
            summary="Search words by text or level",
            description="""
                Search for words in the dictionary by English text (partial match) **or** by level.
                - `search_by`: "word" or "level"
                - `value`: for "word", any text; for "level", must be 'beginner' or 'intermediate'
                - Pagination: `page` and `limit`
            """)
def search_words(
    search_by: str,          # "word" or "level"
    value: str,              # text to search or level
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    """
    Unified search for words. Example:
    /words/search?search_by=word&value=learn
    /words/search?search_by=level&value=beginner
    """
    offset = (page - 1) * limit
    results = crud.filter_words(
        db, search_by, value, offset=offset, limit=limit)
    if not results:
        logger.error("No words found matching your search: %s", value)
        raise HTTPException(
            status_code=404, detail="No words found matching your search.")
    return results


@router.get("/word_of_the_day", response_model=schemas.WordOut,
            summary="Word of the day",
            description="Returns the word of the day (randomly selected, same word for all users for one day).")
def word_of_the_day(
    db: Session = Depends(get_db),
    current_user=Depends(auth.get_current_user),
):
    word = crud.get_word_of_the_day(db)
    if not word:
        raise HTTPException(status_code=404, detail="No words in dictionary.")
    return word


@router.post("/add", response_model=schemas.WordOut,
             summary="Add a new word",
             description="Creates a new word entry. Uses AI to generate translation and details. Admin access required.")
async def add_word(
    word: schemas.WordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.require_admin),
):
    """Add a new Māori word (admin only, AI generated details)."""
    normalized = word.text.strip().lower()
    if crud.get_word_by_normalized(db, normalized):
        logger.warning("Text already exists for input: %s", normalized)
        raise HTTPException(status_code=400, detail="Text already exists")
    result = await ai_integration.get_translation(word.text)
    raw_ai_text = extract_ai_text(result)
    if not raw_ai_text:
        logger.warning(
            "AI did not return a usable response for: %s", raw_ai_text)
        raise HTTPException(
            status_code=502, detail="AI did not return a usable response."
        )
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception:
        logger.error("Failed to parse AI response: %s", ai_data)
        raise HTTPException(
            status_code=502, detail="Failed to parse AI response.")
    ai_data["level"] = sanitize_level(ai_data.get("level"))

    # Step 1: Create word without audio_url to get its ID
    db_word = crud.create_word(
        db, word.text, ai_data, ai_data["level"], audio_url=None)
    db.refresh(db_word)  # Get the generated id from DB
    return db_word
'''
    # Step 2: Generate audio file named after db_word.id
    audio_url = None
    try:
        filename = await ai_integration.synthesize_maori_audio_with_polly(
            ai_data.get("translation", ""),
            # <--- Use word id as filename!
            filename_override=f"{db_word.id}.mp3",
        )
        audio_url = f"/static/audio/{filename}"
        # Step 3: Update db_word with the audio URL
        db_word.audio_url = audio_url
        db.commit()
        db.refresh(db_word)
    except Exception as e:
        # Audio generation failed, just proceed without audio
        pass
        '''

      # Return the (possibly updated) DB object


@router.post("/words/{word_id}/generate_audio_polly", tags=["Words"],
             summary="Generate word audio with Polly",
             description="Generates an audio file for the Māori translation using Amazon Polly. Admin access required.")
async def generate_word_audio_polly(
    word_id: int,
    db: Session = Depends(auth.get_db),
    current_user=Depends(auth.require_admin),
):
    """Generate Polly audio for a word (admin only)."""
    word = db.query(models.Word).filter_by(id=word_id).first()
    normalized = word.text.strip().lower()
    if crud.get_word_by_normalized(db, normalized):
        logger.warning("Translation already exists for: %s", normalized)
        raise HTTPException(
            status_code=400, detail="Translation already exists")
    if not word:
        logger.warning("Word not found for: %s", normalized)
        raise HTTPException(status_code=404, detail="Word not found.")
    maori_text = word.translation
    if not maori_text:
        logger.warning(
            "No translation available for this word: %s", maori_text)
        raise HTTPException(
            status_code=400, detail="No translation available for this word."
        )
    try:
        filename = synthesize_maori_audio_with_polly(maori_text)
        word.audio_url = f"/static/audio/{filename}"
        db.commit()
        return {
            "audio_url": word.audio_url,
            "disclaimer": "Audio generated using Amazon Polly English voice. Māori pronunciation may not be accurate.",
        }
    except Exception as e:
        logger.error("Polly audio generation failed for: %s", maori_text)
        raise HTTPException(
            status_code=500, detail=f"Polly audio generation failed: {e}"
        )


@router.post(
    "/batch_add",
    response_model=schemas.BatchWordResult,
    tags=["Words"],
    description="""
                    **Note:**  
                    - The recommended batch size is 5–10 words at a time.  
                    - The maximum allowed is 15 words per batch to be safe.  
                    - Words that already exist will be skipped and reported in the result."""
)
async def batch_add_words(
    batch: schemas.BatchWordCreate,
    db: Session = Depends(get_db),
    current_user=Depends(auth.require_admin),
):
    added = []
    skipped = []
    for text in batch.texts:
        normalized = text.strip().lower()
        if crud.get_word_by_normalized(db, normalized):
            skipped.append(text)
            logger.info("Skipped (exists): %s", text)
            continue
        try:
            result = await ai_integration.get_translation(text)
            raw_ai_text = extract_ai_text(result)
            if not raw_ai_text:
                logger.warning(
                    "AI did not return usable response for: %s", text)
                skipped.append(text)
                continue
            ai_data = extract_json_from_markdown(raw_ai_text)
            ai_data = sanitize_ai_data(ai_data)
            ai_data["level"] = sanitize_level(ai_data.get("level"))
            db_word = crud.create_word(
                db, text, ai_data, ai_data["level"], audio_url=None)
            db.refresh(db_word)
            added.append(db_word)
            '''
            # Optional: Generate audio
            try:
                filename = await ai_integration.synthesize_maori_audio_with_polly(
                    ai_data.get("translation", ""),
                    filename_override=f"{db_word.id}.mp3",
                )
                db_word.audio_url = f"/static/audio/{filename}"
                db.commit()
                db.refresh(db_word)
            except Exception as e:
                logger.warning("Audio failed for word '%s': %s", text, e)
            
            '''
        except Exception as e:
            logger.error("Error adding word '%s': %s", text, e)
            skipped.append(text)
            
    return schemas.BatchWordResult(
        added=added,
        skipped=skipped
    )
