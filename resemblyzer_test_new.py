from resemblyzer import preprocess_wav, VoiceEncoder
from resemblyzer.audio import sampling_rate
from spectralcluster import SpectralClusterer
from pathlib import Path

'''
    Create the embed for the audio
'''

#give the file path to your audio file
audio_file_path = '/home/parallels/Desktop/Parallels Shared Folders/Home/Desktop/Code/Recognition/audios/Silence_Test.wav'
wav_fpath = Path(audio_file_path)

wav = preprocess_wav(wav_fpath)
encoder = VoiceEncoder("cpu")
_, cont_embeds, wav_splits = encoder.embed_utterance(wav, return_partials=True, rate=16)
#print(cont_embeds.shape)

'''
    Clustering the d-vectors using Spectral Clustering
'''

clusterer = SpectralClusterer(
    min_clusters=2,
    max_clusters=7,
    autotune=None,
    laplacian_type=None,
    refinement_options=None,
    custom_dist="cosine")

# got our labels
labels = clusterer.predict(cont_embeds)

'''
    Create continuous segments
'''
def create_labelling(labels,wav_splits):
    times = [((s.start + s.stop) / 2) / sampling_rate for s in wav_splits]
    labelling = []
    start_time = 0

    for i,time in enumerate(times):
        if i>0 and labels[i]!=labels[i-1]:
            temp = [str(labels[i-1]),start_time,time]
            labelling.append(tuple(temp))
            start_time = time
        if i==len(times)-1:
            temp = [str(labels[i]),start_time,time]
            labelling.append(tuple(temp))

    return labelling

# a list of tuples with values in order (speaker_label,start_time,end_time)
labelling = create_labelling(labels,wav_splits)
print(labelling)

