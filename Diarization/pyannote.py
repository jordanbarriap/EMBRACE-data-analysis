# python==3.8

import os
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment, notebook

import matplotlib.pyplot as plt

pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization")

# apply pretrained pipeline
dir = os.path.dirname(os.getcwd())
WAV_FILE = os.path.join(dir, 'audios/enh_norm_record-672279722.51811_enhanced.wav')
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

# Plot with denser x ticks
import math
import numpy as np
figure, ax = plt.subplots()
figure.set_size_inches(30,4)
end_time = result[-1][1]
ax.set_xticks(np.arange(0, math.ceil(end_time),5))
notebook.plot_annotation(annotation, ax=ax, time=True, legend=True)
figure.savefig('Figure_1_enh+norm.png')