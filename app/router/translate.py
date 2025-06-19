from fastapi import APIRouter
import logging

from app.ai_integration import get_translation
from app.schemas import TranslationRequest, TranslationResponse

from ..utils import extract_ai_text, extract_json_from_markdown, sanitize_ai_data

router = APIRouter(tags=["Translate"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=TranslationResponse,
             summary="Translate word or phrase",
             description="Translates an English word or phrase to Māori using AI.")
async def translate_word(request: TranslationRequest):
    """Translate an English word/phrase to Māori via AI."""
    # Call your AI or translation logic here
    result = await get_translation(request.text)
    raw_ai_text = extract_ai_text(result)
    if not raw_ai_text:
        logger.warning("Translation not found for: %s", raw_ai_text)
        return {"translation": "Translation not found."}
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception:
        logger.error("Error parsing translation for: %s", raw_ai_text)
        return {"translation": "Error parsing translation."}
    # Assume ai_data has a 'translation' field
    return TranslationResponse(**ai_data)
