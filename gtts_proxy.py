import pyttsx3
import os


def create_audio(title, content):
    audio = f"{title}.\n{content}"

    engine = pyttsx3.init()
    engine.setProperty('rate', 200)

    engine.save_to_file(audio, 'output.wav')

    engine.runAndWait()