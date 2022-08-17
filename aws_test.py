import time
import boto3
import json
import urllib
import os

# Convert the json output to be in csv, which is more readable
import tscribe
import csv

# read the api key
with open('aws_rootkey.csv') as f:
    content = f.readlines()

keys = {}
for line in content:
    pair = line.strip().split('=')
    keys.update({pair[0] : pair[1]})

AWS_ACCESS_KEY_ID = keys['AWSAccessKeyId']
AWS_SECRET_KEY = keys['AWSSecretKey']


def transcribe_file(job_name, file_uri, output_file, transcribe_client):
    '''
        Starts an AWS Transcribe job

        Parameters: 
        job_name: set the job name to be whatever that's different from any existed jobs
        file_uri: the file uri of the audio file stored in AWS S3
        output_file: the output file that will be storing the json output
        transcribe_client: an initialized transcribe client
    '''

    # Check if the job wiht the same name has existed
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
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)
                # text = data['results']['transcripts'][0]['transcript']
                # print('======= below is the output =======')
                # print(text)
                # print("===================================")
                
            break
        else:
            print(f"Waiting for {job_name}. Current status is {job_status}.")
        time.sleep(10)

def process_output(output_file, output_csv):
    '''
        Process the json output to be in readable csv

        Parameters:
        output_file: json output file
        output_csv: csv output file

    '''
    # REMEMBER TO CHANGE HERE
    # change json file name and save_as every time we convert a new file
    tscribe.write(output_file, format='csv', save_as=output_csv)

    # sort the csv rows according to sentences' starting time, since before now they are randomly arranged
    rows = []

    # REMEMBER TO CHANGE HERE
    with open(output_csv) as csv_file:
        csv_reader = csv.reader(csv_file)

        # append each row as a list to a bigger list
        line = 0
        for row in csv_reader:
            if line != 0:
                row.pop(0)
                rows.append(row)
            line += 1

    sentences = dict()

    # convert every inner list into an item inside of a big dictionary, and use the start time as keys
    for row in rows:
        sentences[row[0]] = row

    # sort the keys 
    time_keys = sorted(sentences.keys())

    output_list = []

    for key in time_keys:
        output_list.append(sentences[key])

    # opening the csv file in 'w+' mode for reading and writing
    file = open(output_csv, 'w+', newline ='')
    # writing the data into the csv file
    with file:   
        write = csv.writer(file)
        write.writerows(output_list)
    
def main():
    '''
        initiate the transcription work.
        Change the file_url(in asw s3) and job_name every time we initiate a new job
        We will need to manually upload the audio to S3 and copy the file_uri
    '''

    # instantiate the AWS S3 client
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name='us-east-2'
        )
    
    upload_file_bucket = 'kyz1008'
    file_path = 'Diarization/2_noisereduce.wav'
    s3_filename = '2_noisereduce.wav'
    s3_client.upload_file(Filename=file_path, Bucket=upload_file_bucket, Key=s3_filename)

    # retrieve the file uri in S3
    file_uri = 's3://kyz1008/' + s3_filename



    # instantiate the AWS Transcribe service client
    transcribe_client = boto3.client(
        'transcribe',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_KEY,
        region_name='us-east-2'
        )

    # locate the parent directory
    dir = os.path.dirname(os.getcwd())

    output_file = dir + '/aws_output2.json'
    transcribe_file('audio_2', file_uri, output_file, transcribe_client)
    print("===json output has been printed out===")

    # (optional) convert the json output to csv output
    output_csv = dir + '/aws_output2.csv'
    process_output(output_file, output_csv)
    print("===csv output has been printed out===")

if __name__=='__main__':
    main()