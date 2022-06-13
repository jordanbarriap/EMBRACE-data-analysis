from resemblyzer import VoiceEncoder, preprocess_wav
from pathlib import Path
import numpy as np

#give the file path to your audio file
fpath = Path('/home/parallels/Desktop/Parallels Shared Folders/Home/Desktop/Code/Recognition/audios/Silence Test.wav')
wav = preprocess_wav(fpath)

encoder = VoiceEncoder()
embed = encoder.embed_utterance(wav)
np.set_printoptions(precision=3, suppress=True)
print(embed)