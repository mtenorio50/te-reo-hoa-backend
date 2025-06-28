import hashlib
import os
import logging
from typing import Optional
from fastapi import APIRouter, HTTPException, Query, Depends
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app import auth, schemas
from app.ai_integration import synthesize_maori_audio_with_polly
from app.database import get_db

logger = logging.getLogger(__name__)

router = APIRouter(tags=["TTS"])

# Audio cache directory
AUDIO_CACHE_DIR = "./static/audio/tts_cache/"
os.makedirs(AUDIO_CACHE_DIR, exist_ok=True)


def generate_cache_key(text: str, voice_id: str = "Aria") -> str:
    """Generate a unique cache key for the given text and voice."""
    content = f"{text.lower().strip()}_{voice_id}"
    return hashlib.md5(content.encode('utf-8')).hexdigest()


def get_cached_audio_path(cache_key: str) -> Optional[str]:
    """Check if cached audio file exists and return its path."""
    filename = f"tts_{cache_key}.mp3"
    filepath = os.path.join(AUDIO_CACHE_DIR, filename)
    
    if os.path.exists(filepath):
        return filepath
    return None


async def generate_and_cache_audio(text: str, voice_id: str, cache_key: str) -> str:
    """Generate audio using AWS Polly and cache it."""
    try:
        # Generate filename for caching
        filename = f"tts_{cache_key}.mp3"
        
        # Use existing Polly function with filename override
        generated_filename = await synthesize_maori_audio_with_polly(
            maori_text=text,
            voice_id=voice_id,
            output_format="mp3",
            filename_override=filename
        )
        
        # Move the file to cache directory
        original_path = os.path.join("./static/audio/", generated_filename)
        cache_path = os.path.join(AUDIO_CACHE_DIR, filename)
        
        if os.path.exists(original_path) and original_path != cache_path:
            os.rename(original_path, cache_path)
        
        return cache_path
        
    except Exception as e:
        logger.error(f"Failed to generate audio for text '{text}': {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Audio generation failed: {str(e)}"
        )


@router.get("/tts",
           response_model=schemas.TTSResponse,
           summary="Text-to-Speech for Māori",
           description="""
           Convert Māori text to speech using AWS Polly.
           
           **Features:**
           - Caches generated audio files to avoid regeneration
           - Supports different voice options
           - Returns direct audio URL for browser playback
           - **Open access - no authentication required**
           
           **Parameters:**
           - `text`: The Māori text to convert to speech (max 500 characters)
           - `voice_id`: AWS Polly voice ID (default: "Aria")
           - `format`: Output format (default: "mp3")
           
           **Example:**
           ```
           GET /tts/tts?text=Kia ora, he aha to ingoa?
           ```
           """)
async def text_to_speech(
    text: str = Query(..., description="Māori text to convert to speech", max_length=500),
    voice_id: str = Query("Aria", description="AWS Polly voice ID"),
    format: str = Query("mp3", description="Audio format (mp3)")
):
    """
    Convert Māori text to speech using AWS Polly with caching.
    
    This endpoint generates audio from Māori text and caches the result.
    Subsequent requests with the same text will return the cached audio instantly.
    """
    
    # Validate inputs
    if not text or not text.strip():
        raise HTTPException(status_code=400, detail="Text parameter is required")
    
    text = text.strip()
    if len(text) > 500:
        raise HTTPException(status_code=400, detail="Text too long (max 500 characters)")
    
    # Generate cache key
    cache_key = generate_cache_key(text, voice_id)
    
    # Check if audio is already cached
    cached_path = get_cached_audio_path(cache_key)
    
    if cached_path:
        # Return cached audio
        audio_url = f"/static/audio/tts_cache/tts_{cache_key}.mp3"
        logger.info(f"Returning cached audio for text: '{text[:50]}...'")
        
        return schemas.TTSResponse(
            audio_url=audio_url,
            text=text,
            voice_id=voice_id,
            cached=True,
            message="Audio retrieved from cache"
        )
    else:
        # Generate new audio
        logger.info(f"Generating new audio for text: '{text[:50]}...'")
        
        try:
            audio_path = await generate_and_cache_audio(text, voice_id, cache_key)
            audio_url = f"/static/audio/tts_cache/tts_{cache_key}.mp3"
            
            return schemas.TTSResponse(
                audio_url=audio_url,
                text=text,
                voice_id=voice_id,
                cached=False,
                message="Audio generated and cached successfully"
            )
            
        except Exception as e:
            logger.error(f"TTS generation failed: {e}")
            raise HTTPException(
                status_code=500,
                detail="Failed to generate audio. Please try again later."
            )


@router.get("/tts/audio/{cache_key}",
           summary="Direct audio file access",
           description="Direct access to cached audio files by cache key")
async def get_audio_file(
    cache_key: str
):
    """
    Direct access to cached audio files.
    This endpoint allows direct download/streaming of cached audio files.
    """
    
    cached_path = get_cached_audio_path(cache_key)
    
    if not cached_path:
        raise HTTPException(
            status_code=404,
            detail="Audio file not found. It may have been deleted or never generated."
        )
    
    return FileResponse(
        path=cached_path,
        media_type="audio/mpeg",
        filename=f"tts_{cache_key}.mp3"
    )


@router.delete("/tts/cache",
              summary="Clear TTS cache",
              description="Clear all cached TTS audio files. Admin access required.")
async def clear_tts_cache(
    current_user=Depends(auth.require_admin)
):
    """
    Clear all cached TTS audio files (admin only).
    This will force regeneration of all audio files on next request.
    """
    
    try:
        deleted_count = 0
        
        if os.path.exists(AUDIO_CACHE_DIR):
            for filename in os.listdir(AUDIO_CACHE_DIR):
                if filename.startswith("tts_") and filename.endswith(".mp3"):
                    file_path = os.path.join(AUDIO_CACHE_DIR, filename)
                    os.remove(file_path)
                    deleted_count += 1
        
        logger.info(f"Cleared TTS cache: {deleted_count} files deleted")
        
        return {
            "message": f"Successfully cleared TTS cache",
            "deleted_files": deleted_count
        }
        
    except Exception as e:
        logger.error(f"Failed to clear TTS cache: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to clear cache"
        )


@router.get("/tts/cache/info",
           summary="TTS cache information",
           description="Get information about the TTS cache")
async def get_cache_info():
    """
    Get information about the current TTS cache.
    Returns cache size, number of files, etc.
    """
    
    try:
        total_files = 0
        total_size = 0
        
        if os.path.exists(AUDIO_CACHE_DIR):
            for filename in os.listdir(AUDIO_CACHE_DIR):
                if filename.startswith("tts_") and filename.endswith(".mp3"):
                    file_path = os.path.join(AUDIO_CACHE_DIR, filename)
                    if os.path.exists(file_path):
                        total_files += 1
                        total_size += os.path.getsize(file_path)
        
        # Convert bytes to MB
        total_size_mb = round(total_size / (1024 * 1024), 2)
        
        return {
            "cache_directory": AUDIO_CACHE_DIR,
            "total_cached_files": total_files,
            "total_cache_size_mb": total_size_mb,
            "cache_enabled": True
        }
        
    except Exception as e:
        logger.error(f"Failed to get cache info: {e}")
        raise HTTPException(
            status_code=500,
            detail="Failed to retrieve cache information"
        ) 