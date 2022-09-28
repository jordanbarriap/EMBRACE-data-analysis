from pydub import AudioSegment
# for pyannote
import os
from pyannote.audio import Pipeline
from pyannote.core import Annotation, Segment, notebook

import matplotlib.pyplot as plt

from pyannote_test import diarization

# Load the audio.
dir = os.path.dirname(os.getcwd())
WAV_FILE= os.path.join(dir, 'audios/record-667269360.9571331.wav')
song = AudioSegment.from_wav(WAV_FILE)

# pydub does things in milliseconds
# a list containing different lists of human voice chunks (removing the iPad chunks)
# TODO: unreproducible hard-coded values
human_seconds = [song[35 * 1000:61* 1000], song[76 * 1000: ]]

human_song = human_seconds[0]
# iterate over the chunk, concatenate them one by one to a new audio
if len(human_seconds) > 1:
    for chunk in human_seconds[1:]:
        human_song += chunk

# TODO: incorrect export path!!
# export the new audio
human_song.export("2_noipd.wav", format="wav")
# diarize the audio without iPad voice
diarization('2_noipd.wav', 'Figure_2_noipd.png')