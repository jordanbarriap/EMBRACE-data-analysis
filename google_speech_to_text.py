# Imports the Google Cloud client library
from asyncio import subprocess
from google.cloud import speech


"""Transcribe the given audio file."""
import os
from google.cloud import speech
import io
import sys

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "KEY.json"

# Instantiates a client
client = speech.SpeechClient()

with io.open("audios/record-672279722.51811.flac", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

diarization_config = speech.SpeakerDiarizationConfig(
  enable_speaker_diarization=True,
  min_speaker_count=2,
  max_speaker_count=10,
)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=44100,
    language_code="en-US",
    diarization_config=diarization_config,
    audio_channel_count=2,
    enable_automatic_punctuation = True,
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
sys.stdout = open('google_En_output.txt', 'w')
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print(u"Transcript: {}".format(result.alternatives[0].transcript))

sys.stdout.close()