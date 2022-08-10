# python==3.8

from ast import increment_lineno
import os
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment, notebook
from pyannote.core.notebook import repr_annotation

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# apply pretrained pipeline
dir = os.path.dirname(os.getcwd())
WAV_FILE = dir + '/audios/3_speakers.wav'
diarization = pipeline(WAV_FILE)

# print the result
result = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    result.append([float("{:.1f}".format(turn.start)), float("{:.1f}".format(turn.end)),speaker])

'''
    Below is the output(only diarization) for the first real audio. It shows more speakers than it actually is, but it's at some point accurate! It successfully tells the child's voice apart,
    and it's capable to show the overlapping part.
'''
# start=0.5s stop=7.8s speaker_SPEAKER_00
# start=9.0s stop=10.6s speaker_SPEAKER_03
# start=11.3s stop=12.8s speaker_SPEAKER_03
# start=13.0s stop=14.0s speaker_SPEAKER_03
# start=16.1s stop=18.8s speaker_SPEAKER_00
# start=19.0s stop=19.0s speaker_SPEAKER_00
# start=19.9s stop=20.3s speaker_SPEAKER_00
# start=20.4s stop=20.5s speaker_SPEAKER_00
# start=24.0s stop=25.9s speaker_SPEAKER_04
# start=26.6s stop=26.9s speaker_SPEAKER_04
# start=26.9s stop=27.2s speaker_SPEAKER_06
# start=28.0s stop=29.9s speaker_SPEAKER_06
# start=30.8s stop=32.2s speaker_SPEAKER_07
# start=32.2s stop=32.7s speaker_SPEAKER_05
# start=33.7s stop=36.8s speaker_SPEAKER_05
# start=36.6s stop=38.5s speaker_SPEAKER_02
# start=38.8s stop=45.2s speaker_SPEAKER_01
# start=44.3s stop=44.4s speaker_SPEAKER_02
# start=44.4s stop=44.4s speaker_SPEAKER_06
# start=44.4s stop=44.4s speaker_SPEAKER_02
# start=44.4s stop=44.5s speaker_SPEAKER_06
# start=44.5s stop=44.8s speaker_SPEAKER_02
# start=44.8s stop=44.9s speaker_SPEAKER_06
# start=44.9s stop=45.0s speaker_SPEAKER_02
# start=45.2s stop=49.5s speaker_SPEAKER_02
# start=56.1s stop=57.0s speaker_SPEAKER_07

# Producing annotation graph
annotation = Annotation()
for i in result:
    annotation[Segment(i[0], i[1])] = i[2]

# Get `png` data for `annotation`
png_data = repr_annotation(annotation)
# load raw data into a BytesIO container to wrap that data to make it work like a file obkect
img = mpimg.imread(BytesIO(png_data))

# Adjust the width
notebook.width = 40
plt.rcParams['figure.figsize'] = (notebook.width, 2)

imgplot = plt.imshow(img)
plt.show()