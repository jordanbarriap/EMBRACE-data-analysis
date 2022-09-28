from pydub import AudioSegment
# for pyannote
import os
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment, notebook

import matplotlib.pyplot as plt

from pyannote_test import diarization

# Load the audio.
song = AudioSegment.from_wav('audios/record-672279722.51811.wav')

# pydub does things in milliseconds
# a list containing different lists of human voice chunks (removing the iPad chunks)
# TODO: unreproducible hard-coded values
human_seconds = [song[21 * 1000:51* 1000]]

human_song = human_seconds[0]
# iterate over the chunk, concatenate them one by one to a new audio
if len(human_seconds) > 1:
    for chunk in human_seconds[1:]:
        human_song += chunk

# TODO: incorrect export path!!
# export the new audio
human_song.export("1_noipd.wav", format="wav")
# diarize the audio without iPad voice
diarization('1_noipd.wav', 'Figure_1_noipd.png')