from collections import defaultdict
import json

# convert the json into a dict object
with open('ibm_transcript.json') as json_file:
    data = json.load(json_file)

'''
a speaker contains a label(int) and an utterance(a list of dict)
'''
class speaker:
    def __init__(self, label, utterance):
        self.label = label
        self.utterance = utterance


speakers = defaultdict(speaker)

# "results" is a list, and it's elements are intervals(dict)!
print(data['results'][0]['alternatives'][0]['timestamps'])

# print(data["speaker_labels"])


