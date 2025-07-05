from app.database import SessionLocal
from app import models, ai_integration, crud
import asyncio


"""
Used this code to generate data for ipa and phonetics only.
"""


async def update_word_pronunciation(word):
    # If you want to use just pronunciation guide:
    # pron = await ai_integration.get_pronunciation_guide(word.translation)
    # word.ipa = pron.get("ipa", "")
    # word.phonetic = pron.get("phonetic", "")
    # Or if you want to use get_translation (to possibly update everything):
    try:
        ai_response = await ai_integration.get_translation(word.text)
        # extract_ai_text and extract_json_from_markdown are your utility functions
        from app.utils import extract_ai_text, extract_json_from_markdown
        raw_ai_text = extract_ai_text(ai_response)
        ai_data = extract_json_from_markdown(raw_ai_text)
        word.ipa = ai_data.get("ipa", "")
        word.phonetic = ai_data.get("phonetic", "")
        print(
            f"Updated: {word.text} → IPA: {word.ipa}, Phonetic: {word.phonetic}")
        return True
    except Exception as e:
        print(f"Error updating {word.text}: {e}")
        return False


def main():
    db = SessionLocal()
    words = db.query(models.Word).filter(
        (models.Word.ipa == None) | (models.Word.ipa == '') |
        (models.Word.phonetic == None) | (models.Word.phonetic == '')
    ).all()
    print(f"{len(words)} words to update.")
    loop = asyncio.get_event_loop()
    for word in words:
        loop.run_until_complete(update_word_pronunciation(word))
        db.commit()  # Commit after each, or batch up if preferred
    db.close()


if __name__ == "__main__":
    main()
