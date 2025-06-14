# app/utils.py
import json
import re


def extract_json_from_markdown(md_text: str) -> dict:
    """Extracts JSON object from markdown or plaintext AI response."""
    clean = re.sub(r"^```(?:json)?\s*", "",
                   md_text.strip(), flags=re.IGNORECASE)
    clean = re.sub(r"\s*```$", "", clean.strip())
    return json.loads(clean)


def sanitize_ai_data(ai_data: dict) -> dict:
    """Ensures all expected keys exist and are non-None strings."""
    fields = ["translation", "type", "domain", "example", "notes"]
    for f in fields:
        ai_data[f] = str(ai_data.get(f) or "")
    return ai_data


def extract_ai_text(result: dict) -> str:
    """Safely extracts the AI response text from Gemini API result."""
    try:
        candidates = result.get("candidates")
        if not candidates or not isinstance(candidates, list):
            raise ValueError("No candidates in AI response")
        content = candidates[0].get("content")
        if not content or "parts" not in content or not content["parts"]:
            raise ValueError("No content parts in AI response")
        return content["parts"][0].get("text", "")
    except Exception as e:
        print("AI response extraction failed:", e)
        print("Full response:", result)
        return ""
