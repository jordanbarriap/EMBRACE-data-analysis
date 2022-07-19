import wave
import audio_metadata

def frame_rate_channel(audio_file_name):
    print(audio_file_name)
    with wave.open(audio_file_name, "rb") as wave_file:
        frame_rate = wave_file.getframerate()
        channels = wave_file.getnchannels()
        return frame_rate,channels

# print(frame_rate_channel('audios/record-672279722.51811.flac'))

metadata = audio_metadata.load('audios/record-672279722.51811.flac')
print(metadata)
