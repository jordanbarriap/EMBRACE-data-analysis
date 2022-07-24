import time
import boto3
import json
import urllib

# read the api key
with open('aws_rootkey.csv') as f:
    content = f.readlines()

keys = {}
for line in content:
    pair = line.strip().split('=')
    keys.update({pair[0] : pair[1]})

AWS_ACCESS_KEY_ID = keys['AWSAccessKeyId']
AWS_SECRET_KEY = keys['AWSSecretKey']


def transcribe_file(job_name, file_uri, transcribe_client):
    '''
    Starts an AWS Transcribe job
    '''

    existed_jobs = transcribe_client.list_transcription_jobs()['TranscriptionJobSummaries']

    job_existed = False

    for job in existed_jobs:
        if job['TranscriptionJobName'] == job_name:
            job_existed = True

    if job_existed is False:
        transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': file_uri},
            MediaFormat='wav',
            LanguageOptions=['es-ES' ,'en-US'],
            IdentifyMultipleLanguages = True,
            Settings = {
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 4
            }
        )

    max_tries = 20
    while max_tries > 0:
        max_tries -= 1
        job = transcribe_client.get_transcription_job(TranscriptionJobName=job_name)
        job_status = job['TranscriptionJob']['TranscriptionJobStatus']
        if job_status in ['COMPLETED', 'FAILED']:
            print(f"Job {job_name} is {job_status}.")
            if job_status == 'COMPLETED':
                # print(
                #     f"Download the transcript from\n"
                #     f"\t{job['TranscriptionJob']['Transcript']['TranscriptFileUri']}.")
                response = urllib.request.urlopen(job['TranscriptionJob']['Transcript']['TranscriptFileUri'])
                data = json.loads(response.read())
                with open('aws_output.json', 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                # text = data['results']['transcripts'][0]['transcript']
                # print('======= below is the output =======')
                # print(text)
                # print("===================================")
                
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)
    
def main():
    # instantiate the AWS Transcribe service client
    transcribe_client = boto3.client(
        'transcribe',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name='us-east-2'
        )
    file_uri = 's3://kyz1008/record-672279722.51811.wav'
    transcribe_file('test', file_uri, transcribe_client)

if __name__=='__main__':
    main()