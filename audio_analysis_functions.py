import parselmouth

import numpy as np
import matplotlib.pyplot as plt

import seaborn as sns

from pydub import AudioSegment
from pydub.playback import play

import math

import time

from pyannote.audio import Pipeline

#Function that helps on filtering pitch for a certain range of frequencies (low_pitch_threshold as minimum and high_pitch_threshold as maximum)
def extract_pitch_segments(pitch,low_pitch_threshold,high_pitch_threshold):
    secs_audio = pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    secs_pitch = []
    filtered_pitch_values = []
    index_pitch_values = []
    for i in range(0,len(pitch_values)):
        freq = pitch_values[i]
        if math.isnan(freq)!=True and (freq>=low_pitch_threshold and freq<=high_pitch_threshold):
            secs_pitch.append(secs_audio[i])
            filtered_pitch_values.append(pitch_values[i])
            index_pitch_values.append(i)
        if math.isnan(freq)!=True and secs_audio[i]>=274 and secs_audio[i]<=278:
            print(str(secs_audio[i])+": "+str(freq))
    return secs_pitch,filtered_pitch_values,index_pitch_values

#Get the avg pitch of a certain audio chunk, enhanced if you have a subset of parts where there is an active voice
def avg_pitch(pitch,min_voice_freq,max_voice_freq,active_voice_list):
    secs_audio = pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    sum_freqs = 0
    n_valid_freqs = 0
    for act_info in active_voice_list:
        start_active=act_info[0]
        end_active=act_info[1]
        for i in range(0,len(pitch_values)):
            freq = pitch_values[i]
            sec = secs_audio[i]
            if math.isnan(freq)!=True and (sec>=start_active and sec<=end_active) and (freq>=min_voice_freq and freq<=max_voice_freq):
                sum_freqs = sum_freqs + float(freq)
                n_valid_freqs = n_valid_freqs + 1
    avg_pitch = -1
    if n_valid_freqs>0:
        avg_pitch = sum_freqs/n_valid_freqs
    print("Avg pitch: "+str(avg_pitch))
    return avg_pitch

#Get the median pitch (quantile 0.5)  of the audio chunk given as input, enhanced if you have a subset of parts where there is an active voice
def median_pitch(pitch,min_voice_freq,max_voice_freq,active_voice_list):
    secs_audio = pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    secs_freqs_tuple = extract_pitch_subset(pitch,active_voice_list)
    freqs_list = secs_freqs_tuple[1]
    #Remove NaNs from the list
    freqs_list_clean = [x for x in freqs_list if np.isnan(x)==False]
    median_pitch = -1
    if len(freqs_list_clean)>0:
        median_pitch = np.median(freqs_list_clean)
    print("Median pitch: "+str(median_pitch))
    return median_pitch

#Get a certain quantile of the audio chunk given as input
def quantile_pitch(pitch,min_voice_freq,max_voice_freq,active_voice_list,quantile):
    secs_audio = pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    secs_freqs_tuple = extract_pitch_subset(pitch,active_voice_list)
    freqs_list = secs_freqs_tuple[1]
    freqs_list_clean = [x for x in freqs_list if np.isnan(x)==False]
    quantile_pitch = -1
    if len(freqs_list_clean)>0:
        quantile_pitch = np.quantile(freqs_list_clean,quantile/100)
    #print("Quartile "+str(quantile)+": "+str(quantile_pitch))
    return quantile_pitch

#Extract a certain segment of audio samples between two times within the audio
def extract_pitch_subset(pitch,seconds_start_end_tuple):
    secs_audio = pitch.xs()
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values==0] = np.nan
    sub_secs_audio = []
    sub_pitch_values = []

    act_info = seconds_start_end_tuple
    start_active=act_info[0]
    end_active=act_info[1]
    #print("Time segment: "+str(start_active)+","+str(end_active))
    for i in range(0,len(pitch_values)):
        freq = pitch_values[i]
        sec = secs_audio[i]
        if sec>=start_active and sec<=end_active:
            sub_secs_audio.append(sec)
            sub_pitch_values.append(freq)

    return (sub_secs_audio,sub_pitch_values)

def classify_audio_freq(avg_freq):
    label =  "-"
    #I used 15 hz less from the actual minimum threshold for each category
    if(avg_freq>=60 and avg_freq<170):#Male adult minimum is 85
        label = "am|rms|rme"
    elif(avg_freq>=170 and avg_freq<250):#Female adult minimum is 165
        label = "af|rfs|rfe"
    elif(avg_freq>=255 and avg_freq<=500):#Child minimum is 250
        label = "c"
    #print(label)
    return label

#Returns the timespans within a specific audio where there is actual voice being played
def get_voice_activity(filename,print_timespans_option,play_option):
    pipeline_act_detection = Pipeline.from_pretrained("pyannote/voice-activity-detection",
                                        use_auth_token="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")

    output = pipeline_act_detection(filename)
    audio = AudioSegment.from_wav(filename)

    voice_act_tuples_list = []

    for speech in output.get_timeline().support():
        # active speech between speech.start and speech.end
        if(print_timespans_option):
            print(speech)
        if(play_option):
            play_audio_segment(audio,speech.start*1000,speech.end*1000)
        voice_act_tuples_list.append((speech.start,speech.end))
    return voice_act_tuples_list

#Create custom-size chunks
def custom_size_segments(voice_segments):
    chunk_size = 1
    custom_active_voice_segments = []
    for segment in voice_segments:
        start_segment = segment[0]
        end_segment = segment[1]
        time_duration = end_segment - start_segment
        if time_duration<1:
            custom_active_voice_segments.append(segment)
        else:
            start_aux = start_segment
            end_aux = start_segment + 1
            while start_aux < end_segment:
                custom_active_voice_segments.append((start_aux,end_aux))
                start_aux = start_aux + 1
                end_aux = end_aux + 1
                if end_aux>end_segment:
                    end_aux = end_segment

    #print all the small segments
    total_custom_segments = 0
    for custom_segment in custom_active_voice_segments:
        #print(custom_segment)
        total_custom_segments = total_custom_segments + 1
    print("Total custom-size segments: "+str(total_custom_segments))
    return custom_active_voice_segments

def play_audio_segment(audio,start_milliseconds,end_milliseconds):
    audio_segment = audio[start_milliseconds:end_milliseconds]
    play(audio_segment)

def play_audio_segment_by_index(audio,audio_segments,index):
    audio_segment = audio_segments[index]
    play_audio_segment(audio,audio_segment[0]*1000,audio_segment[1]*1000)

def play_and_plot_audio_segment_by_index(audio,pitch,audio_segments,index):
    #play the audio segment
    audio_segment = audio_segments[index]
    play_audio_segment(audio,audio_segment[0]*1000,audio_segment[1]*1000)

    #plot the pitch in that segment
    secs_and_pitch_values = extract_pitch_subset(pitch,audio_segment)
    plt.plot(secs_and_pitch_values[0], secs_and_pitch_values[1], 'o', markersize=2)
    plt.show()