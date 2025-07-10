import pytest
import json
from datetime import datetime
from unittest.mock import AsyncMock, patch
from app.ai_integration import get_translation
from app.utils import sanitize_ai_data, extract_json_from_markdown, extract_ai_text
from app.router.words import add_word, batch_add_words
from app.schemas import WordCreate, BatchWordCreate


class TestIPAPhoneticHandling:
    """Test suite for IPA and phonetic data handling with multi-word phrases."""

    @pytest.fixture
    def mock_gemini_response_single_word(self):
        """Mock Gemini response for single word 'hello'."""
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "translation": "kia ora",
                            "ipa": "ˈkia ˈɔɾa",
                            "phonetic": "kee-ah or-ah",
                            "type": "greeting",
                            "domain": "greetings",
                            "example": "Kia ora! How are you? / Hello! How are you?",
                            "notes": "Common greeting in New Zealand"
                        })
                    }]
                }
            }]
        }

    @pytest.fixture
    def mock_gemini_response_multi_word(self):
        """Mock Gemini response for multi-word phrase 'good morning'."""
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "translation": "ata mārie",
                            "ipa": "ˈata ˈmaːɾie",
                            "phonetic": "ah-tah mah-ree-eh",
                            "type": "greeting",
                            "domain": "greetings",
                            "example": "Ata mārie! Good morning!",
                            "notes": "Morning greeting, literally means 'calm dawn'"
                        })
                    }]
                }
            }]
        }

    @pytest.fixture
    def mock_gemini_response_missing_ipa(self):
        """Mock Gemini response missing IPA/phonetic data."""
        return {
            "candidates": [{
                "content": {
                    "parts": [{
                        "text": json.dumps({
                            "translation": "aroha",
                            "type": "noun",
                            "domain": "emotions",
                            "example": "He aroha nui taku ki a koe",
                            "notes": "Love, compassion"
                            # Missing ipa and phonetic fields
                        })
                    }]
                }
            }]
        }

    @pytest.mark.asyncio
    async def test_get_translation_single_word_with_ipa(self, mock_gemini_response_single_word):
        """Test that single word translation preserves IPA and phonetic data."""
        with patch('app.ai_integration.gemini_post', return_value=mock_gemini_response_single_word):
            result = await get_translation("hello")

            # Extract and parse the response
            raw_text = extract_ai_text(result)
            ai_data = extract_json_from_markdown(raw_text)
            sanitized_data = sanitize_ai_data(ai_data)

            assert sanitized_data["translation"] == "kia ora"
            assert sanitized_data["ipa"] == "ˈkia ˈɔɾa"
            assert sanitized_data["phonetic"] == "kee-ah or-ah"
            assert sanitized_data["type"] == "greeting"
            assert sanitized_data["domain"] == "greetings"

    @pytest.mark.asyncio
    async def test_get_translation_multi_word_with_ipa(self, mock_gemini_response_multi_word):
        """Test that multi-word phrase translation preserves IPA and phonetic data."""
        with patch('app.ai_integration.gemini_post', return_value=mock_gemini_response_multi_word):
            result = await get_translation("good morning")

            # Extract and parse the response
            raw_text = extract_ai_text(result)
            ai_data = extract_json_from_markdown(raw_text)
            sanitized_data = sanitize_ai_data(ai_data)

            assert sanitized_data["translation"] == "ata mārie"
            assert sanitized_data["ipa"] == "ˈata ˈmaːɾie"
            assert sanitized_data["phonetic"] == "ah-tah mah-ree-eh"
            assert sanitized_data["type"] == "greeting"
            assert sanitized_data["domain"] == "greetings"

    def test_sanitize_ai_data_preserves_ipa_phonetic(self):
        """Test that sanitize_ai_data preserves IPA and phonetic fields."""
        """Test that sanitize_ai_data preserves IPA and phonetic fields."""
        raw_data = {
            "translation": "kia ora",
            "ipa": "ˈkia ˈɔɾa",
            "phonetic": "kee-ah or-ah",
            "type": "greeting",
            "domain": "greetings",
            "example": "Kia ora!",
            "notes": "Common greeting"
        }

        sanitized = sanitize_ai_data(raw_data)

        # Verify all fields are preserved
        assert sanitized["translation"] == "kia ora"
        assert sanitized["ipa"] == "ˈkia ˈɔɾa"
        assert sanitized["phonetic"] == "kee-ah or-ah"
        assert sanitized["type"] == "greeting"
        assert sanitized["domain"] == "greetings"
        assert sanitized["example"] == "Kia ora!"
        assert sanitized["notes"] == "Common greeting"

    def test_sanitize_ai_data_handles_missing_ipa_phonetic(self):
        """Test that sanitize_ai_data handles missing IPA and phonetic fields gracefully."""
        """Test that sanitize_ai_data handles missing IPA and phonetic fields gracefully."""
        raw_data = {
            "translation": "aroha",
            "type": "noun",
            "domain": "emotions"
            # Missing ipa, phonetic, example, notes
        }

        sanitized = sanitize_ai_data(raw_data)

        # Verify missing fields are set to empty strings
        assert sanitized["translation"] == "aroha"
        assert sanitized["ipa"] == ""  # Should be empty string, not missing
        # Should be empty string, not missing
        assert sanitized["phonetic"] == ""
        assert sanitized["type"] == "noun"
        assert sanitized["domain"] == "emotions"
        assert sanitized["example"] == ""
        assert sanitized["notes"] == ""

    def test_add_word_endpoint_with_ipa_phonetic(self, client, register_and_login_admin, db_session, mock_gemini_response_multi_word):
        """Test add_word endpoint preserves IPA and phonetic data in database."""
        """Test add_word endpoint preserves IPA and phonetic data in database."""
        with patch('app.ai_integration.gemini_post', return_value=mock_gemini_response_multi_word):
            token = register_and_login_admin

            response = client.post(
                "/words/add",
                json={"text": "good morning"},
                headers={"Authorization": f"Bearer {token}"}
            )

            # Debug: print response details if it fails
            if response.status_code != 200:
                print(f"Response status: {response.status_code}")
                print(f"Response text: {response.text}")

            assert response.status_code == 200
            data = response.json()

            # Verify the word was created with IPA and phonetic data
            assert data["text"] == "good morning"
            assert data["translation"] == "ata mārie"
            assert data["ipa"] == "ˈata ˈmaːɾie"
            assert data["phonetic"] == "ah-tah mah-ree-eh"
            assert data["type"] == "greeting"
            assert data["domain"] == "greetings"

    def test_batch_add_words_with_ipa_phonetic(self, client, register_and_login_admin, db_session):
        """Test batch_add_words preserves IPA and phonetic data for multiple words."""
        """Test batch_add_words preserves IPA and phonetic data for multiple words."""

        # Mock responses for different words
        mock_responses = {
            "hello": {
                "candidates": [{
                    "content": {
                        "parts": [{
                            "text": json.dumps({
                                "translation": "kia ora",
                                "ipa": "ˈkia ˈɔɾa",
                                "phonetic": "kee-ah or-ah",
                                "type": "greeting",
                                "domain": "greetings",
                                "example": "Kia ora!",
                                "notes": "Common greeting"
                            })
                        }]
                    }
                }]
            },
            "thank you": {
                "candidates": [{
                    "content": {
                        "parts": [{
                            "text": json.dumps({
                                "translation": "ngā mihi",
                                "ipa": "ˈŋaː ˈmihi",
                                "phonetic": "nga mee-hee",
                                "type": "phrase",
                                "domain": "greetings",
                                "example": "Ngā mihi for your help",
                                "notes": "Formal thanks"
                            })
                        }]
                    }
                }]
            }
        }

        async def mock_gemini_post(payload, *args, **kwargs):
            # Extract the word being translated from the prompt
            prompt_text = payload["contents"][0]["parts"][0]["text"]
            if "hello" in prompt_text:
                return mock_responses["hello"]
            elif "thank you" in prompt_text:
                return mock_responses["thank you"]
            else:
                raise ValueError(f"Unexpected word in prompt: {prompt_text}")

        with patch('app.ai_integration.gemini_post', side_effect=mock_gemini_post):
            token = register_and_login_admin

            response = client.post(
                "/words/batch_add",
                json={"texts": ["hello", "thank you"]},
                headers={"Authorization": f"Bearer {token}"}
            )

            assert response.status_code == 200
            data = response.json()

            # Verify both words were added
            assert len(data["added"]) == 2
            assert len(data["skipped"]) == 0

            # Verify first word (hello -> kia ora)
            word1 = data["added"][0]
            assert word1["text"] == "hello"
            assert word1["translation"] == "kia ora"
            assert word1["ipa"] == "ˈkia ˈɔɾa"
            assert word1["phonetic"] == "kee-ah or-ah"

            # Verify second word (thank you -> ngā mihi)
            word2 = data["added"][1]
            assert word2["text"] == "thank you"
            assert word2["translation"] == "ngā mihi"
            assert word2["ipa"] == "ˈŋaː ˈmihi"
            assert word2["phonetic"] == "nga mee-hee"

    def test_extract_ai_text_from_valid_response(self, mock_gemini_response_multi_word):
        """Test that extract_ai_text properly extracts text from Gemini response."""
        extracted_text = extract_ai_text(mock_gemini_response_multi_word)

        # Should be valid JSON string
        assert extracted_text.strip().startswith('{')
        assert extracted_text.strip().endswith('}')

        # Should be parseable as JSON
        parsed = json.loads(extracted_text)
        assert "translation" in parsed
        assert "ipa" in parsed
        assert "phonetic" in parsed

    def test_extract_json_from_markdown_with_clean_json(self):
        """Test that extract_json_from_markdown handles clean JSON correctly."""
        clean_json = '{"translation": "kia ora", "ipa": "ˈkia ˈɔɾa", "phonetic": "kee-ah or-ah"}'

        result = extract_json_from_markdown(clean_json)

        assert result["translation"] == "kia ora"
        assert result["ipa"] == "ˈkia ˈɔɾa"
        assert result["phonetic"] == "kee-ah or-ah"

    def test_extract_json_from_markdown_with_code_fences(self):
        """Test that extract_json_from_markdown handles JSON with markdown code fences."""
        markdown_json = '''```json
{
    "translation": "ata mārie",
    "ipa": "ˈata ˈmaːɾie",
    "phonetic": "ah-tah mah-ree-eh",
    "type": "greeting"
}
```'''

        result = extract_json_from_markdown(markdown_json)

        assert result["translation"] == "ata mārie"
        assert result["ipa"] == "ˈata ˈmaːɾie"
        assert result["phonetic"] == "ah-tah mah-ree-eh"
        assert result["type"] == "greeting"

    @pytest.mark.asyncio
    async def test_prompt_contains_ipa_phonetic_requirements(self):
        """Test that the AI prompt explicitly requests IPA and phonetic data."""

        # Mock the gemini_post to capture the prompt
        captured_prompts = []

        async def capture_prompt(payload, *args, **kwargs):
            captured_prompts.append(payload["contents"][0]["parts"][0]["text"])
            return {
                "candidates": [{
                    "content": {
                        "parts": [{
                            "text": '{"translation": "test", "ipa": "test", "phonetic": "test", "type": "", "domain": "", "example": "", "notes": ""}'
                        }]
                    }
                }]
            }

        with patch('app.ai_integration.gemini_post', side_effect=capture_prompt):
            await get_translation("test phrase")

            prompt = captured_prompts[0]

            # Verify prompt explicitly asks for IPA and phonetic
            assert "ipa" in prompt.lower()
            assert "phonetic" in prompt.lower()
            assert "REQUIRED" in prompt
            assert "multi-word phrases" in prompt
            assert "provide IPA for each word" in prompt
            assert "show how to pronounce each word" in prompt


# Integration test to verify the complete flow
def test_complete_ipa_phonetic_flow(client, register_and_login_admin, db_session):
    """Integration test: Complete flow from API request to database storage with IPA/phonetic."""
    """Integration test: Complete flow from API request to database storage with IPA/phonetic."""

    mock_response = {
        "candidates": [{
            "content": {
                "parts": [{
                    "text": json.dumps({
                        "translation": "he pai tērā",
                        "ipa": "he ˈpai ˈteːɾaː",
                        "phonetic": "heh pie teh-rah",
                        "type": "phrase",
                        "domain": "expressions",
                        "example": "He pai tērā! That's good!",
                        "notes": "Positive expression"
                    })
                }]
            }
        }]
    }

    with patch('app.ai_integration.gemini_post', return_value=mock_response):
        token = register_and_login_admin

        # Add word via API
        response = client.post(
            "/words/add",
            json={"text": "that's good"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        word_data = response.json()
        word_id = word_data["id"]

        # Verify word was stored with IPA and phonetic data
        assert word_data["text"] == "that's good"
        assert word_data["translation"] == "he pai tērā"
        assert word_data["ipa"] == "he ˈpai ˈteːɾaː"
        assert word_data["phonetic"] == "heh pie teh-rah"

        # Retrieve word via API to double-check database storage
        response = client.get(
            f"/words/search?search_by=word&value=that's good")
        assert response.status_code == 200
        search_results = response.json()

        assert len(search_results) == 1
        stored_word = search_results[0]
        assert stored_word["ipa"] == "he ˈpai ˈteːɾaː"
        assert stored_word["phonetic"] == "heh pie teh-rah"
