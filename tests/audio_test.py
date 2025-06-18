import boto3
import os
from dotenv import load_dotenv
load_dotenv('.env')

# Make sure your credentials and region are set up

polly_client = boto3.client("polly", region_name="ap-southeast-2")


def synthesize_and_save(text, voice_id="Aria", output_format="mp3"):
    response = polly_client.synthesize_speech(
        Text=text,
        VoiceId=voice_id,
        OutputFormat=output_format,
        Engine="neural"
    )
    audio_stream = response.get("AudioStream")
    if not audio_stream:
        raise Exception("No audio stream returned from Polly.")
    filename = f"test_polly_{text.replace(' ', '_').lower()}.mp3"
    with open(filename, "wb") as f:
        f.write(audio_stream.read())
    print(f"Audio saved as {filename}")


if __name__ == "__main__":
    maori_text = input("Enter Māori word or phrase to test Polly: ")
    synthesize_and_save(maori_text)
