import requests

"""
    upload the audio file
"""
# filename = "audios/shortmix.wav"
# def read_file(filename, chunk_size=5242880):
#     with open(filename, 'rb') as _file:
#         while True:
#             data = _file.read(chunk_size)
#             if not data:
#                 break
#             yield data

# headers = {'authorization': "2e3e2cdcdb934f28bf47bd2db6718800"}
# response = requests.post('https://api.assemblyai.com/v2/upload',
#                         headers=headers,
#                         data=read_file(filename))

# print(response.json())

"""
    Submit the upload for transcription
"""

# endpoint = "https://api.assemblyai.com/v2/transcript"
# json = {
#     "audio_url": "https://cdn.assemblyai.com/upload/eb6da8ec-d038-4f77-90b3-20424880b7d0",
#     "speaker_labels": True,
#     "language_detection": True
# }
# headers = {
#     "authorization": "2e3e2cdcdb934f28bf47bd2db6718800",
#     "content-type": "application/json"
# }
# response = requests.post(endpoint, json=json, headers=headers)
# print(response.json())

"""
    Get the transcription result
"""
endpoint = "https://api.assemblyai.com/v2/transcript/ol7r52rvs2-adf1-4249-a4d5-c004a9b55d00"
headers = {
    "authorization": "2e3e2cdcdb934f28bf47bd2db6718800",
}
response = requests.get(endpoint, headers=headers)
import json
with open('transcript.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)
print(response.json())