from fastapi import APIRouter, Request
import logging
import traceback
import httpx

from app.ai_integration import get_translation
from app.schemas import TranslationRequest, TranslationResponse

from ..utils import extract_ai_text, extract_json_from_markdown, sanitize_ai_data

router = APIRouter(tags=["Translate"])
logger = logging.getLogger(__name__)


@router.post("/", response_model=TranslationResponse)
async def translate_word(request: TranslationRequest, req: Request):
    try:
        from app.ai_integration import timeout  # make sure you use your timeout
        async with httpx.AsyncClient(timeout=timeout) as client:
            # uses client with timeout
            result = await get_translation(request.text)
        raw_ai_text = extract_ai_text(result)
        if not raw_ai_text:
            return TranslationResponse(translation="Translation not found.")
        try:
            ai_data = extract_json_from_markdown(raw_ai_text)
            ai_data = sanitize_ai_data(ai_data)
        except Exception:
            return TranslationResponse(translation="Error parsing translation.")
        return TranslationResponse(translation=ai_data.get("translation", "No translation found."))
    except httpx.ReadTimeout:
        logger.error("Gemini API timed out:\n" + traceback.format_exc())
        return TranslationResponse(translation="AI service is slow or unavailable, please try again later.")
    except Exception as e:
        logger.error(
            f"Unexpected error in /translate: {e}\n{traceback.format_exc()}")
        return TranslationResponse(translation="Internal server error.")
