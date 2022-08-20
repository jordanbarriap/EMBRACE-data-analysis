import soundfile as sf
import matplotlib.pyplot as plt

from simple_diarizer.diarizer import Diarizer
from simple_diarizer.utils import combined_waveplot

import os
import wave
import librosa
from pydub import AudioSegment

dir = os.path.dirname(os.getcwd())

WAV_FILE = dir + '/audios/record-672279722.51811.wav'
sound = AudioSegment.from_wav(WAV_FILE)
sound = sound.set_channels(1)
sound.export(dir + '/audios/record_downsampling.wav', format='wav')

data, sr = librosa.load(dir + '/audios/record_downsampling.wav')

diar = Diarizer(
                  embed_model='ecapa', # 'xvec' and 'ecapa' supported
                  cluster_method='sc' # 'ahc' and 'sc' supported
               )


segments = diar.diarize(data, num_speakers=4)

# # signal, fs = sf.read(WAV_FILE)
# # combined_waveplot(signal, fs, segments)
# # plt.show()
# print(segments)