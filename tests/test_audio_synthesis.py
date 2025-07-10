import pytest
import os
import tempfile
import asyncio
from unittest.mock import Mock, patch, MagicMock
from io import BytesIO

from app.ai_integration import synthesize_maori_audio_with_polly
from app.router.tts import generate_cache_key, get_cached_audio_path, generate_and_cache_audio


class TestAudioSynthesis:
    """Test suite for AWS Polly audio synthesis functionality."""

    @pytest.fixture
    def mock_polly_response(self):
        """Mock a successful Polly response."""
        mock_response = {
            "AudioStream": BytesIO(b"fake_audio_data_here")
        }
        return mock_response

    @pytest.fixture
    def mock_polly_client(self, mock_polly_response):
        """Mock the Polly client."""
        with patch('app.ai_integration.polly_client') as mock_client:
            mock_client.synthesize_speech.return_value = mock_polly_response
            yield mock_client

    @pytest.fixture
    def temp_audio_dir(self):
        """Create a temporary directory for audio files."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the AUDIO_DIR constant
            with patch('app.ai_integration.AUDIO_DIR', temp_dir):
                yield temp_dir

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_basic(self, mock_polly_client, temp_audio_dir):
        """Test basic audio synthesis with Polly."""
        maori_text = "Kia ora"

        # Call the function
        filename = await synthesize_maori_audio_with_polly(maori_text)

        # Verify Polly was called with correct parameters
        mock_polly_client.synthesize_speech.assert_called_once_with(
            Text=maori_text,
            VoiceId="Aria",
            OutputFormat="mp3",
            Engine="neural"
        )

        # Verify filename format
        expected_filename = f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
        assert filename == expected_filename

        # Verify file was created
        audio_path = os.path.join(temp_audio_dir, filename)
        assert os.path.exists(audio_path)

        # Verify file content
        with open(audio_path, 'rb') as f:
            content = f.read()
            assert content == b"fake_audio_data_here"

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_custom_voice(self, mock_polly_client, temp_audio_dir):
        """Test audio synthesis with custom voice."""
        maori_text = "Kia ora"
        voice_id = "Joanna"

        filename = await synthesize_maori_audio_with_polly(
            maori_text, voice_id=voice_id
        )

        # Verify Polly was called with custom voice
        mock_polly_client.synthesize_speech.assert_called_once_with(
            Text=maori_text,
            VoiceId=voice_id,
            OutputFormat="mp3",
            Engine="neural"
        )

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_custom_format(self, mock_polly_client, temp_audio_dir):
        """Test audio synthesis with custom output format."""
        maori_text = "Kia ora"
        output_format = "wav"

        filename = await synthesize_maori_audio_with_polly(
            maori_text, output_format=output_format
        )

        # Verify Polly was called with custom format
        mock_polly_client.synthesize_speech.assert_called_once_with(
            Text=maori_text,
            VoiceId="Aria",
            OutputFormat=output_format,
            Engine="neural"
        )

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_filename_override(self, mock_polly_client, temp_audio_dir):
        """Test audio synthesis with filename override."""
        maori_text = "Kia ora"
        filename_override = "custom_audio.mp3"

        filename = await synthesize_maori_audio_with_polly(
            maori_text, filename_override=filename_override
        )

        # Verify custom filename is used
        assert filename == filename_override

        # Verify file was created with custom name
        audio_path = os.path.join(temp_audio_dir, filename_override)
        assert os.path.exists(audio_path)

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_multi_word(self, mock_polly_client, temp_audio_dir):
        """Test audio synthesis with multi-word Māori phrases."""
        maori_text = "Kia ora koutou katoa"

        filename = await synthesize_maori_audio_with_polly(maori_text)

        # Verify filename format for multi-word phrases
        expected_filename = f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
        assert filename == expected_filename

        # Verify file was created
        audio_path = os.path.join(temp_audio_dir, filename)
        assert os.path.exists(audio_path)

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_special_characters(self, mock_polly_client, temp_audio_dir):
        """Test audio synthesis with special Māori characters."""
        maori_text = "Tēnā koe"

        filename = await synthesize_maori_audio_with_polly(maori_text)

        # Verify filename format handles special characters
        expected_filename = f"polly_{maori_text.replace(' ', '_').lower()}.mp3"
        assert filename == expected_filename

        # Verify file was created
        audio_path = os.path.join(temp_audio_dir, filename)
        assert os.path.exists(audio_path)

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_no_audio_stream(self, temp_audio_dir):
        """Test handling of missing audio stream in Polly response."""
        with patch('app.ai_integration.polly_client') as mock_client:
            # Mock response with no AudioStream
            mock_client.synthesize_speech.return_value = {}

            with pytest.raises(Exception) as excinfo:
                await synthesize_maori_audio_with_polly("Kia ora")

            assert "No audio stream returned from Polly" in str(excinfo.value)

    @pytest.mark.asyncio
    async def test_synthesize_maori_audio_polly_error(self, temp_audio_dir):
        """Test handling of Polly API errors."""
        with patch('app.ai_integration.polly_client') as mock_client:
            # Mock Polly to raise an exception
            mock_client.synthesize_speech.side_effect = Exception(
                "Polly API error")

            with pytest.raises(Exception) as excinfo:
                await synthesize_maori_audio_with_polly("Kia ora")

            assert "Polly API error" in str(excinfo.value)


class TestTTSCaching:
    """Test suite for TTS caching functionality."""

    def test_generate_cache_key_basic(self):
        """Test basic cache key generation."""
        text = "Kia ora"
        voice_id = "Aria"

        key = generate_cache_key(text, voice_id)

        # Should return a valid MD5 hash
        assert len(key) == 32
        assert key.isalnum()

    def test_generate_cache_key_consistent(self):
        """Test that cache keys are consistent for same inputs."""
        text = "Kia ora"
        voice_id = "Aria"

        key1 = generate_cache_key(text, voice_id)
        key2 = generate_cache_key(text, voice_id)

        assert key1 == key2

    def test_generate_cache_key_different_text(self):
        """Test that different texts produce different cache keys."""
        voice_id = "Aria"

        key1 = generate_cache_key("Kia ora", voice_id)
        key2 = generate_cache_key("Tēnā koe", voice_id)

        assert key1 != key2

    def test_generate_cache_key_different_voice(self):
        """Test that different voices produce different cache keys."""
        text = "Kia ora"

        key1 = generate_cache_key(text, "Aria")
        key2 = generate_cache_key(text, "Joanna")

        assert key1 != key2

    def test_generate_cache_key_case_insensitive(self):
        """Test that cache keys are case insensitive."""
        voice_id = "Aria"

        key1 = generate_cache_key("Kia ora", voice_id)
        key2 = generate_cache_key("KIA ORA", voice_id)

        assert key1 == key2

    def test_generate_cache_key_whitespace_handling(self):
        """Test that cache keys handle whitespace correctly."""
        voice_id = "Aria"

        key1 = generate_cache_key("Kia ora", voice_id)
        key2 = generate_cache_key("  Kia ora  ", voice_id)

        assert key1 == key2

    def test_get_cached_audio_path_exists(self):
        """Test getting cached audio path when file exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create a test audio file
            cache_key = "test_cache_key"
            filename = f"tts_{cache_key}.mp3"
            filepath = os.path.join(temp_dir, filename)

            with open(filepath, 'w') as f:
                f.write("test")

            # Patch the AUDIO_CACHE_DIR
            with patch('app.router.tts.AUDIO_CACHE_DIR', temp_dir):
                result = get_cached_audio_path(cache_key)
                assert result == filepath

    def test_get_cached_audio_path_not_exists(self):
        """Test getting cached audio path when file doesn't exist."""
        with tempfile.TemporaryDirectory() as temp_dir:
            cache_key = "nonexistent_cache_key"

            # Patch the AUDIO_CACHE_DIR
            with patch('app.router.tts.AUDIO_CACHE_DIR', temp_dir):
                result = get_cached_audio_path(cache_key)
                assert result is None

    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_success(self):
        """Test successful audio generation and caching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the synthesize function
            with patch('app.router.tts.synthesize_maori_audio_with_polly') as mock_synthesize:
                with patch('app.router.tts.AUDIO_CACHE_DIR', temp_dir):
                    cache_key = "test_cache_key"
                    filename = f"tts_{cache_key}.mp3"

                    mock_synthesize.return_value = filename

                    # Mock os.path.exists to return False so file move is skipped
                    with patch('app.router.tts.os.path.exists', return_value=False):
                        # Call the function
                        result = await generate_and_cache_audio("Kia ora", "Aria", cache_key)

                        # Verify the function completed and returned expected cache path
                        expected_cache_path = os.path.join(temp_dir, filename)
                        assert result == expected_cache_path

    @pytest.mark.asyncio
    async def test_generate_and_cache_audio_synthesis_error(self):
        """Test handling of synthesis errors in caching."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Mock the synthesize function to raise an error
            with patch('app.router.tts.synthesize_maori_audio_with_polly') as mock_synthesize:
                with patch('app.router.tts.AUDIO_CACHE_DIR', temp_dir):
                    mock_synthesize.side_effect = Exception("Synthesis failed")

                    # Should raise HTTPException
                    with pytest.raises(Exception) as excinfo:
                        await generate_and_cache_audio("Kia ora", "Aria", "test_key")

                    assert "Audio generation failed" in str(excinfo.value)


class TestTTSEndpoint:
    """Test suite for TTS API endpoint."""

    @pytest.fixture
    def mock_synthesize_audio(self):
        """Mock the synthesize_maori_audio_with_polly function."""
        with patch('app.router.tts.synthesize_maori_audio_with_polly') as mock_func:
            mock_func.return_value = "test_audio.mp3"
            yield mock_func

    def test_tts_endpoint_basic(self, client, mock_synthesize_audio):
        """Test basic TTS endpoint functionality."""
        # Mock the caching functions
        with patch('app.router.tts.get_cached_audio_path', return_value=None):
            with patch('app.router.tts.generate_and_cache_audio') as mock_generate:
                mock_generate.return_value = "/path/to/audio.mp3"

                response = client.get("/tts/tts?text=Kia ora")

                assert response.status_code == 200
                data = response.json()

                assert "audio_url" in data
                assert data["text"] == "Kia ora"
                assert data["voice_id"] == "Aria"
                assert data["cached"] is False

    def test_tts_endpoint_cached(self, client):
        """Test TTS endpoint with cached audio."""
        with patch('app.router.tts.get_cached_audio_path', return_value="/cached/audio.mp3"):
            response = client.get("/tts/tts?text=Kia ora")

            assert response.status_code == 200
            data = response.json()

            assert data["cached"] is True
            assert data["message"] == "Audio retrieved from cache"

    def test_tts_endpoint_custom_voice(self, client, mock_synthesize_audio):
        """Test TTS endpoint with custom voice."""
        with patch('app.router.tts.get_cached_audio_path', return_value=None):
            with patch('app.router.tts.generate_and_cache_audio') as mock_generate:
                mock_generate.return_value = "/path/to/audio.mp3"

                response = client.get("/tts/tts?text=Kia ora&voice_id=Joanna")

                assert response.status_code == 200
                data = response.json()

                assert data["voice_id"] == "Joanna"

    def test_tts_endpoint_empty_text(self, client):
        """Test TTS endpoint with empty text."""
        response = client.get("/tts/tts?text=")

        assert response.status_code == 400
        assert "Text parameter is required" in response.json()["detail"]

    def test_tts_endpoint_text_too_long(self, client):
        """Test TTS endpoint with text that's too long."""
        long_text = "a" * 501  # Exceeds 500 character limit

        response = client.get(f"/tts/tts?text={long_text}")

        # FastAPI Query validation returns 422, not 400
        assert response.status_code == 422

    def test_tts_endpoint_missing_text(self, client):
        """Test TTS endpoint without text parameter."""
        response = client.get("/tts/tts")

        assert response.status_code == 422  # Validation error

    def test_tts_endpoint_generation_error(self, client):
        """Test TTS endpoint with generation error."""
        with patch('app.router.tts.get_cached_audio_path', return_value=None):
            with patch('app.router.tts.generate_and_cache_audio') as mock_generate:
                mock_generate.side_effect = Exception("Generation failed")

                response = client.get("/tts/tts?text=Kia ora")

                assert response.status_code == 500
                assert "Failed to generate audio" in response.json()["detail"]


class TestTTSIntegration:
    """Integration tests for TTS functionality."""

    def test_full_tts_workflow(self, client):
        """Test the complete TTS workflow from request to response."""
        maori_text = "Kia ora"

        # Mock caching functions for predictable behavior
        cache_key = "test_cache_key"

        with patch('app.router.tts.generate_cache_key', return_value=cache_key):
            with patch('app.router.tts.get_cached_audio_path') as mock_get_cached:
                with patch('app.router.tts.generate_and_cache_audio') as mock_generate:
                    # First request - no cache
                    mock_get_cached.return_value = None
                    mock_generate.return_value = f"/cache/tts_{cache_key}.mp3"

                    response1 = client.get(f"/tts/tts?text={maori_text}")
                    assert response1.status_code == 200

                    data1 = response1.json()
                    assert data1["text"] == maori_text
                    assert data1["cached"] is False

                    # Second request - cached
                    mock_get_cached.return_value = f"/cache/tts_{cache_key}.mp3"

                    response2 = client.get(f"/tts/tts?text={maori_text}")
                    assert response2.status_code == 200

                    data2 = response2.json()
                    assert data2["text"] == maori_text
                    assert data2["cached"] is True

    @pytest.mark.asyncio
    async def test_real_file_caching_workflow(self):
        """Test the actual file system caching workflow."""
        maori_text = "Kia ora"

        with tempfile.TemporaryDirectory() as temp_dir:
            # Patch the cache directory
            with patch('app.router.tts.AUDIO_CACHE_DIR', temp_dir):
                # Generate cache key
                cache_key = generate_cache_key(maori_text, "Aria")

                # Initially, no cached file should exist
                cached_path = get_cached_audio_path(cache_key)
                assert cached_path is None

                # Create a fake cached file
                filename = f"tts_{cache_key}.mp3"
                filepath = os.path.join(temp_dir, filename)
                with open(filepath, 'w') as f:
                    f.write("fake audio data")

                # Now the cached file should be found
                cached_path = get_cached_audio_path(cache_key)
                assert cached_path == filepath
                assert os.path.exists(cached_path)

    @pytest.mark.asyncio
    async def test_tts_with_maori_characters(self, client):
        """Test TTS with Māori characters and diacritics."""
        maori_text = "Tēnā koe, he aha tō ingoa?"

        with patch('app.ai_integration.polly_client') as mock_polly:
            with patch('app.router.tts.AUDIO_CACHE_DIR', tempfile.mkdtemp()):
                with patch('app.ai_integration.AUDIO_DIR', tempfile.mkdtemp()):
                    mock_polly.synthesize_speech.return_value = {
                        "AudioStream": BytesIO(b"fake_audio_data")
                    }

                    response = client.get(f"/tts/tts?text={maori_text}")
                    assert response.status_code == 200

                    data = response.json()
                    assert data["text"] == maori_text

                    # Verify Polly was called with the correct text
                    mock_polly.synthesize_speech.assert_called_once()
                    call_args = mock_polly.synthesize_speech.call_args
                    assert call_args[1]["Text"] == maori_text

    @pytest.mark.asyncio
    async def test_tts_multiple_voices(self, client):
        """Test TTS with different voice options."""
        maori_text = "Kia ora"
        voices = ["Aria", "Joanna", "Nicole"]

        with patch('app.ai_integration.polly_client') as mock_polly:
            with patch('app.router.tts.AUDIO_CACHE_DIR', tempfile.mkdtemp()):
                with patch('app.ai_integration.AUDIO_DIR', tempfile.mkdtemp()):
                    mock_polly.synthesize_speech.return_value = {
                        "AudioStream": BytesIO(b"fake_audio_data")
                    }

                    for voice in voices:
                        response = client.get(
                            f"/tts/tts?text={maori_text}&voice_id={voice}")
                        assert response.status_code == 200

                        data = response.json()
                        assert data["voice_id"] == voice
                        assert data["text"] == maori_text
