'''
    Separating out silent chunks, and passing them seperately for recognition
'''
from pydub import AudioSegment
from pydub.silence import split_on_silence
from ibm_test import test
import os

# Load the audio.
audio = AudioSegment.from_wav("audios/record-672279722.51811.wav")
dBFS = audio.dBFS       # for calculating relative silence threshold

# spliting audio files, specify that a silent chunk must be at least 2 seconds(2000ms) long, and by default, 
# consider a chunk silent if it's -16 dBFS quieter than the entire dBFS.
audio_chunks = split_on_silence(audio, min_silence_len=1500, silence_thresh=dBFS-16)

# TODO: (decide to do or not) normalize the chunks to have the same dBFS


# Output chunks for transcription
for i, chunk in enumerate(audio_chunks):
    chunk.export(f'slices/{i}_output.wav', format="wav")

directory = 'slices'
filenames = os.listdir(directory)
sorted_filenames = sorted(filenames, key=lambda x: int(x.split('_')[0]))
for filename in sorted_filenames:
    filename = 'slices/'+filename
    test(filename, 'slice_output.json')
    # w.write('-'*50)