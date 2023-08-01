import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

while True:
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    amplitude = np.max(data)
    frequency = np.fft.rfftfreq(CHUNK, d=1.0/RATE)
    spectrum = np.abs(np.fft.rfft(data))
    dominant_frequency = frequency[np.argmax(spectrum)]

    print("Amplitude:", amplitude)
    print("Dominant Frequency:", dominant_frequency)

stream.stop_stream()
stream.close()
p.terminate()
