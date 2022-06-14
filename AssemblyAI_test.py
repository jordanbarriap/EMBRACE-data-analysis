import requests
import json

"""
    upload the audio file
"""
def upload_audio(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'authorization': "2e3e2cdcdb934f28bf47bd2db6718800"}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                            headers=headers,
                            data=read_file(filename))

    # return a dictionary with only one element keeping the upload_url of the audio
    return response.json()

"""
    Submit the upload for transcription
"""
def submit_for_transcription(upload_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": upload_url,
        "speaker_labels": True,
        "language_detection": True
    }
    headers = {
        "authorization": "2e3e2cdcdb934f28bf47bd2db6718800",
        "content-type": "application/json"
    }
    response = requests.post(endpoint, json=json, headers=headers)
    #print(response.json())

"""
    Get the transcription result
"""
def get_transcript(endpoint):
    headers = {
        "authorization": "2e3e2cdcdb934f28bf47bd2db6718800",
    }
    response = requests.get(endpoint, headers=headers)
    return response

'''
    Main steps
'''
upload_url = upload_audio("audios/overlap.wav")['upload_url']
submit_for_transcription(upload_url)

# retrive endpoint from AssemblyAI account processing queue
endpoint = "https://api.assemblyai.com/v2/transcript/otlhsaml0k-4f87-4a71-9a3a-ed722577a74c"
response = get_transcript(endpoint)

with open('AssemblyAI_transcript.json', 'w', encoding='utf-8') as f:
    json.dump(response.json(), f, ensure_ascii=False, indent=4)
