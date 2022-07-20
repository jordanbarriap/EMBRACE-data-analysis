from google.cloud import speech_v1p1beta1 as speech
import os
import sys

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = "KEY.json"

client = speech.SpeechClient()

speech_file = "audios/record-672279722.51811.flac"

# first_lang = "en-US"
# second_lang = "es"

with open(speech_file, "rb") as audio_file:
    content = audio_file.read()

audio = speech.types.RecognitionAudio(content=content)

diarization_config = speech.types.SpeakerDiarizationConfig(
  enable_speaker_diarization=True,
  min_speaker_count=3,
#   max_speaker_count=3,
)


config = speech.types.RecognitionConfig(
    encoding=speech.types.RecognitionConfig.AudioEncoding.FLAC,
    sample_rate_hertz=44100,
    language_code='en-US',
    # alternative_language_codes=[second_lang],
    diarization_config=diarization_config,
    audio_channel_count=2,
    # enable_separate_recognition_per_channel=True,
    enable_word_confidence=True,
)

print("Waiting for operation to complete...")
response = client.recognize(config=config, audio=audio)

# The transcript within each result is separate and sequential per result.
# However, the words list within an alternative includes all the words
# from all the results thus far. Thus, to get all the words with speaker
# tags, you only have to take the words list from the last result:
result = response.results[-1]

words_info = result.alternatives[0].words

sys.stdout = open('google_En_output.txt', 'w')
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
    print(
        u"First Word and Confidence: ({}, {})".format(
            alternative.words[0].word, alternative.words[0].confidence
        )
    )
    print(u"Channel Tag: {}".format(result.channel_tag))

sys.stdout.close()