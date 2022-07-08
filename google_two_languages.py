from google.cloud import speech_v1p1beta1 as speech
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "KEY.json"

client = speech.SpeechClient()

speech_file = "audios/record-672279722.51811.wav"
first_lang = "es"
second_lang = "en-US"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.RecognitionAudio(content=content)

config = speech.RecognitionConfig(
    encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=44100,
    audio_channel_count=2,
    language_code=first_lang,
    alternative_language_codes=[second_lang],
    #enable_speaker_diarization=True,
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

f = open("google_2lang_output.txt", "w")


for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    f.write("-" * 20)
    f.write("\n")
    f.write(u"First alternative of result {}: {} \n".format(i, alternative))
    f.write(u"Transcript: {} \n".format(alternative.transcript))

f.close()