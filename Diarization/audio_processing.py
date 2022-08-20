# 1. Reduce the noise (noisereduce or speech_recognition)
# 2. Adjust the whole audio to make pieces at the same pitch (pydub)
# 3. Feed the processed audio into pyannote

from scipy.io import wavfile
import os

from pydub import AudioSegment, effects

import noisereduce as nr
import speech_recognition as sr

# get the input file
dir = os.path.dirname(os.getcwd())
WAV_FILE = dir + '/audios/record-672279722.51811.wav'

sample_rate, data = wavfile.read(WAV_FILE)
# only works with mono audio, and assume our both channels record the same thing
if len(data.shape) > 1:
    left_channel = data[:,0]


def reduce_noise(nr_des_wav_file):
    '''
        apply noisereduce

        Parameters: 
        des_wav_file: stores the output wav file that gets noise reduced
    '''
    # noisereduce
    reduced_noise = nr.reduce_noise(y = left_channel, sr=sample_rate, thresh_n_mult_nonstationary=2,stationary=False)
    wavfile.write(nr_des_wav_file, sample_rate, reduced_noise)

def speech_recognition(sr_des_wav_file):
    '''
        apply adjust_for_ambient_noise of speech recognition

        Parameters: 
        des_wav_file: stores the output wav file that gets noise reduced
    '''
    # speech recognition
    recognizer = sr.Recognizer()
    test_audio_file = sr.AudioFile(WAV_FILE)

    with test_audio_file as source:
        recognizer.adjust_for_ambient_noise(source, duration=0.5)
        audio_data = recognizer.record(source)
    # write audio to a WAV file
    with open(sr_des_wav_file, "wb") as f:
        f.write(audio_data.get_wav_data())

def normalize_volume(norm_des_file, normalize_method):
    '''
        Normalize Volume

        Parameters:
        norm_des_file: output file storing the normalized audio
        normalize_method: 'max' or 'manual', either scale the whole audio to the max amplitude or manually set an amplitude
    '''
    # audio = AudioSegment.from_wav(WAV_FILE)
    # dBFS = audio.dBFS  # get the dBFS for this entire audio

    if normalize_method == 'max':
        # scale the whole audio to the max amplitude.
        _sound = AudioSegment.from_file(WAV_FILE, "wav")
        sound = effects.normalize(_sound)
        sound.export(norm_des_file, format="wav")

    if normalize_method == 'manual':
        # another approach: manually set the amplitude
        def match_target_amplitude(sound, target_dBFS):
            change_in_dBFS = target_dBFS - sound.dBFS
            return sound.apply_gain(change_in_dBFS)

        sound = AudioSegment.from_file(WAV_FILE, "wav")
        normalized_sound = match_target_amplitude(sound, -10.0)
        normalized_sound.export(norm_des_file, format="wav")

def main():
    # test noisereduce
    nr_des_wav_file = '1_noisereduce.wav'
    reduce_noise(nr_des_wav_file)

    # # test speech recognition's noise reduction
    # sr_des_wav_file = '2_speechrecognition.wav'
    # speech_recognition(sr_des_wav_file)

    # # Normalize volume
    # norm_des_file = '2_reduce_normalize_volume.wav'
    # normalize_method = 'max'
    # normalize_volume(norm_des_file, normalize_method)

if __name__=='__main__':
    main()