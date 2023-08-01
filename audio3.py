import sounddevice as sd
import numpy as np
import librosa

def callback(indata, frames, time, status):
    amplitude = np.max(indata)
    frequency = librosa.pitch_tuning(np.array(indata), sr=44100)

    print("Amplitude:", amplitude)
    print("Frequency:", frequency)

with sd.InputStream(callback=callback):
    sd.sleep(duration * 1000)
