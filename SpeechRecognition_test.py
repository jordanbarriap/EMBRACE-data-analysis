import speech_recognition as sr

recognizer = sr.Recognizer()

test_audio_file = sr.AudioFile('audios/audio_files_harvard.wav')

# adjust for ambient noise pass in the file
with test_audio_file as source:
    recognizer.adjust_for_ambient_noise(source, duration = 0.5)
    audio_data = recognizer.record(source)
    result = recognizer.recognize_google(audio_data = audio_data)
    print(result)
