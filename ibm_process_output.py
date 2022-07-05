from collections import defaultdict
import json

# convert the json into a dict object
with open('ibm_transcript.json') as json_file:
    data = json.load(json_file)

'''
a speaker contains a label(int) and an utterance(a list of dict)
'''
class speaker:
    def __init__(self, label=None, utterance=None):
        self.label = label
        self.utterance = utterance
    
    def __str__(self):
        return f'This is speaker {self.label} saying {self.utterance}'


speakers = defaultdict(speaker)
intervals = []

# "results" is a list, and it's elements are intervals(dict)!
# the list of all intervals. We can calculate the time from it
for interval in data['results']:
    intervals.append(interval)

# for every timestamp in every interval, create a speaker object and use the start time as key
for interval in data['results']:
    for timestamp in interval['alternatives'][0]['timestamps']:
        utterance = {'text': timestamp[0], 'from': timestamp[1], 'to': timestamp[2]}
        speakers[timestamp[1]] = speaker(None, utterance)

# corresponds the text with speaker labels, which is a list
for label in data['speaker_labels']:
    speakers[label['from']].label = label['speaker']

for k, v in speakers.items():
    print(f'{v}')