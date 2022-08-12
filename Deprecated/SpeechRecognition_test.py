import speech_recognition as sr

recognizer = sr.Recognizer()

test_audio_file = sr.AudioFile('audios/record-672279722.51811.wav')

# adjust for ambient noise pass in the file
with test_audio_file as source:
    # recognizer.adjust_for_ambient_noise(source)
    audio_data = recognizer.record(source)
    result = recognizer.recognize_google(audio_data = audio_data, language='en-US')
    print(result)
