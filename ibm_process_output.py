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


timepoints = defaultdict(speaker)
intervals = []

# "results" is a list, and it's elements are intervals(dict)!
# the list of all intervals. We can calculate the time from it
for interval in data['results']:
    intervals.append(interval)

# for every timestamp in every interval, create a speaker object and use the start time as key
for interval in data['results']:
    for timestamp in interval['alternatives'][0]['timestamps']:
        utterance = {'text': timestamp[0], 'from': timestamp[1], 'to': timestamp[2]}
        timepoints[timestamp[1]] = speaker(None, utterance)

# corresponds the text with speaker labels, which is a list
for label in data['speaker_labels']:
    timepoints[label['from']].label = label['speaker']

# get the result based on the timepoints
for v in timepoints.values():
    print(f'{v}')

# get the result based on the speaker(s)
speakers = defaultdict(list)
for utter in timepoints.values():
    speakers[f'speaker_label:{utter.label}'].append(utter.utterance)
    

with open('ibm_speaker_output.json','w', encoding='utf-8') as f:
    json.dump(speakers, f, ensure_ascii=False, indent=4)