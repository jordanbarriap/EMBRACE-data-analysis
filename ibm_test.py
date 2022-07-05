# depentencies import
from ibm_watson import SpeechToTextV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator
import json

api_key = 'r1xA04K1GHDn8_sATEA5qcF8u1mSSOvm3IuyEJMXpR9W'
url = 'https://api.au-syd.speech-to-text.watson.cloud.ibm.com/instances/bacb3fff-7963-483c-9197-e7feb05ad805'

authenticator = IAMAuthenticator(api_key)
stt = SpeechToTextV1(authenticator=authenticator)
stt.set_service_url(url)

file_name = "/home/kangying/Desktop/Code/AudioProcessing/audios/record-672279722.51811.wav"

with open(file_name, 'rb') as f:
    res = stt.recognize(audio=f, content_type='audio/wav', speaker_labels=True, model='es-MX_NarrowbandModel').get_result()
    print(type(res))

with open('ibm_transcript.json', 'w', encoding='utf-8') as f:
    json.dump(res, f, ensure_ascii=False, indent=4)