import speech_recognition as sr
import pyaudio
import wave
import difflib
from words2 import wordsListEn
from words2 import wordsListAr
from pynput.keyboard import Key, Listener

def recordSound():
    chunk = 1024  # Record in chunks of 1024 samples
    sample_format = pyaudio.paInt16  # 16 bits per sample
    channels = 2
    fs = 44100  # Record at 44100 samples per second
    seconds = 2
    filename = "output.wav"

    p = pyaudio.PyAudio()  # Create an interface to PortAudio

    print('Recording')

    stream = p.open(format=sample_format,
                    channels=channels,
                    rate=fs,
                    frames_per_buffer=chunk,
                    input=True)

    frames = []  # Initialize array to store frames

    # Store data in chunks for 3 seconds
    for i in range(0, int(fs / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)

    # Stop and close the stream 
    stream.stop_stream()
    stream.close()
    # Terminate the PortAudio interface
    p.terminate()

    print('Finished recording')

    # Save the recorded data as a WAV file
    wf = wave.open(filename, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(p.get_sample_size(sample_format))
    wf.setframerate(fs)
    wf.writeframes(b''.join(frames))
    wf.close()

r = sr.Recognizer()

def on_press(key):
    if key != Key.shift and key != Key.alt_l:
        return
    try:
        print("----------------------------------------")
        print("----------------------------------------")
        print("----------------------------------------")
        recordSound()

        with sr.AudioFile('output.wav') as source:
            audio = r.record(source)

        if key==Key.shift:
            textEn = r.recognize_google(audio, language='en-US')
            print("Google predection 1: ", textEn)
            matchesEn = difflib.get_close_matches(textEn, [*wordsListEn])
            for match in matchesEn:
                print(match, wordsListEn[match][::-1])

        if key==Key.alt_l:
            textAr = r.recognize_google(audio, language='ar-SA')
            print("Google predection 2: ", textAr[::-1])
            matchesAr = difflib.get_close_matches(textAr, [*wordsListAr])
            for match in matchesAr:
                print(match[::-1], wordsListAr[match])
    except Exception as e:
        print(e)
        print("Exception, please try again")

def on_release(key):
    pass

with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()