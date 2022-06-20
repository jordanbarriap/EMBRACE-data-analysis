# Imports the Google Cloud client library
from asyncio import subprocess
from google.cloud import speech

# Instantiates a client
client = speech.SpeechClient.from_service_account_file('/Users/zikangying/Desktop/Code/NLP/KEY.json')

file_name = 'NLP/audios/3_speakers.wav'

with open(file_name, 'rb') as f:
    audio_data = f.read()

audio_file = speech.RecognitionAudio(content = audio_data)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    #sample_rate_hertz=16000,
    language_code="en-US",
    enable_automatic_punctuation = True,
)

subprocess.call(['avconv', '-i', file_name, '-y', '-ar', '48000', '-ac', '1', 'last.flac'])

# Detects speech in the audio file
response = client.recognize(config=config, audio=audio_file)

for result in response.results:
    print("Transcript: {}".format(result.alternatives[0].transcript))

"""Transcribe the given audio file."""
import os
from google.cloud import speech
import io

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/zikangying/Desktop/Code/NLP/KEY.json"

client = speech.SpeechClient()

with io.open("/Users/zikangying/Desktop/Code/NLP/audios/3_speakers.wav", "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

diarization_config = speech.SpeakerDiarizationConfig(
  enable_speaker_diarization=True,
  min_speaker_count=2,
  max_speaker_count=10,
)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=16000,
    language_code="en-US",
    diarization_config=diarization_config,
)

response = client.recognize(config=config, audio=audio)

# Each result is for a consecutive portion of the audio. Iterate through
# them to get the transcripts for the entire audio file.
for result in response.results:
    # The first alternative is the most likely one for this portion.
    print(u"Transcript: {}".format(result.alternatives[0].transcript))