# python==3.8

import os
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment, notebook
# from pyannote.core.notebook import repr_annotation

import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from io import BytesIO

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# apply pretrained pipeline
dir = os.path.dirname(os.getcwd())
WAV_FILE = dir + '/audios/record-667269360.9571331.wav'
diarization = pipeline(WAV_FILE)

# print the result
result = []
for turn, _, speaker in diarization.itertracks(yield_label=True):
    # print(f"start={turn.start:.1f}s stop={turn.end:.1f}s speaker_{speaker}")
    result.append([float("{:.1f}".format(turn.start)), float("{:.1f}".format(turn.end)),speaker])

# Producing annotation graph
annotation = Annotation()
for i in result:
    annotation[Segment(i[0], i[1])] = i[2]

# # Get `png` data for `annotation`
# png_data = repr_annotation(annotation)
# # load raw data into a BytesIO container to wrap that data to make it work like a file obkect
# img = mpimg.imread(BytesIO(png_data))

# # Adjust the width
# notebook.width = 40
# plt.rcParams['figure.figsize'] = (notebook.width, 2)

# imgplot = plt.imshow(img)
# plt.show()

# Plot with denser x ticks
import math
import numpy as np
figure, ax = plt.subplots()
figure.set_size_inches(30,4)
end_time = result[-1][1]
ax.set_xticks(np.arange(0, math.ceil(end_time),5))
notebook.plot_annotation(annotation, ax=ax, time=True, legend=True)
figure.savefig('Figure_2.png')