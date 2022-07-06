from collections import defaultdict
from math import sqrt
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
# intervals = []

# "results" is a list, and it's elements are intervals(dict)!
# # the list of all intervals. We can calculate the time from it
# for interval in data['results']:
#     intervals.append(interval)

# for every timestamp in every interval, create a speaker object and use the start time as key
for interval in data['results']:
    for timestamp in interval['alternatives'][0]['timestamps']:
        utterance = {'text': timestamp[0], 'from': timestamp[1], 'to': timestamp[2]}
        timepoints[timestamp[1]] = speaker(None, utterance)

# corresponds the text with speaker_labels, which is a list
for label in data['speaker_labels']:
    timepoints[label['from']].label = label['speaker']

# get the result based on the timepoints
for v in timepoints.values():
    print(f'{v}')

# get the result based on the speaker(s)
speakers = defaultdict(list)
speaker_set = set()
for utter in timepoints.values():
    speakers[f'speaker_label:{utter.label}'].append(utter.utterance)
    speaker_set.add(utter.label)

with open('ibm_speaker_output.json','w', encoding='utf-8') as f:
    json.dump(speakers, f, ensure_ascii=False, indent=4)

# calculate ave words per speaker interval using timepoints
num_speakers = len(speaker_set)
num_intervals = [0]*num_speakers   # the number of intervals for each speaker
num_words = [0]*num_speakers       # the number of words for each speaker

num_words_intervals = []           # contains lists of words in every interval, for each speaker
for speaker in range(num_speakers):
    num_words_intervals.append([])

last_label = None
for aspeaker in timepoints.values():
    curr_label = aspeaker.label
    # there is a speaker change
    if last_label != curr_label:
        num_intervals[curr_label]+=1                # add an interval
        num_words_intervals[curr_label].append(0)   # start a new words counter for this new interval
    num_words[curr_label]+=1
    num_words_intervals[curr_label][-1]+=1          # increment the last counter

    last_label = curr_label

# Mean
for speaker in range(num_speakers):
    print(f'The average number of words per interval for speaker {speaker} is {num_words[speaker]/num_intervals[speaker]}' )

# Standard deviation
for speaker in range(num_speakers):
    mean = num_words[speaker]/num_intervals[speaker]
    variance = sum((x - mean) ** 2 for x in num_words_intervals[speaker]) / num_intervals[speaker]
    std_dev = sqrt(variance)
    print(f'The standard deviation of words per interval for speaker {speaker} is {std_dev}')