# depentencies import
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
# import speech_recognition as sr
import json
import os

api_key = 'r1xA04K1GHDn8_sATEA5qcF8u1mSSOvm3IuyEJMXpR9W'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/bacb3fff-7963-483c-9197-e7feb05ad805'

authenticator = IAMAuthenticator(api_key)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

file_name = 'audios/record-672279722.51811.flac'

# recognizer = sr.Recognizer()
# recognizer.energy_threshold = 4000


# test_audio_file = sr.AudioFile(file_name)

# # adjust for ambient noise pass in the file
# with test_audio_file as source:
#     recognizer.adjust_for_ambient_noise(source, duration = 0.5)
#     audio_data = recognizer.record(source)

with open(file_name, 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/flac', speaker_labels=True, model='es-LA_Telephony', background_audio_suppression = 0.4).get_result()

with open('ibm_transcript_noise_suppression.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)