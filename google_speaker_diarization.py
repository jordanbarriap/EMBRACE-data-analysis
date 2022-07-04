from google.cloud import speech_v1p1beta1 as speech
import os
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "/Users/zikangying/Desktop/Code/NLP/KEY.json"

client = speech.SpeechClient()

speech_file = "/Users/zikangying/Desktop/Code/NLP/audios/output.wav"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)

diarization_config = speech.types.SpeakerDiarizationConfig(
  enable_speaker_diarization=True,
  min_speaker_count=3,
  max_speaker_count=3,
)


config = speech.types.RecognitionConfig(
    encoding=speech.types.RecognitionConfig.AudioEncoding.LINEAR16,
    sample_rate_hertz=48000,
    language_code="en-US",
    # diarization_config=diarization_config,
    audio_channel_count=3,
    enable_separate_recognition_per_channel=True,
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

# Printing out the output:
for word_info in words_info:
    print(
        u"word: '{}', speaker_tag: {}".format(word_info.word, word_info.speaker_tag)
    )

for i, result in enumerate(response.results):
    alternative = result.alternatives[0]
    print("-" * 20)
    print("First alternative of result {}".format(i))
    print(u"Transcript: {}".format(alternative.transcript))
    print(u"Channel Tag: {}".format(result.channel_tag))