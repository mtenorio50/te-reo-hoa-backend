from fastapi import APIRouter
from app.schemas import TranslationRequest, TranslationResponse
from app.ai_integration import get_translation
from ..utils import sanitize_ai_data, extract_json_from_markdown, extract_ai_text


router = APIRouter(tags=["Translate"])


@router.post("/", response_model=TranslationResponse)
async def translate_word(request: TranslationRequest):
    # Call your AI or translation logic here
    result = await get_translation(request.text)
    raw_ai_text = extract_ai_text(result)
    if not raw_ai_text:
        return {"translation": "Translation not found."}
    try:
        ai_data = extract_json_from_markdown(raw_ai_text)
        ai_data = sanitize_ai_data(ai_data)
    except Exception:
        return {"translation": "Error parsing translation."}
    # Assume ai_data has a 'translation' field
    return TranslationResponse(**ai_data)
