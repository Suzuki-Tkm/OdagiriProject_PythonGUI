import pyaudio
import numpy as np

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
DURATION = 10  # 10秒間の平均値を取得する

p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

frames = []  # データのフレームを保存するリスト
duration_frames = RATE * DURATION  # 10秒間のフレーム数
frames_received = 0  # 取得したフレーム数のカウンタ

while True:
    data = np.frombuffer(stream.read(CHUNK), dtype=np.int16)
    frames.append(data)
    frames_received += len(data)

    if frames_received >= duration_frames:
        frames = np.concatenate(frames)[:duration_frames]  # 必要なフレーム数だけ取得
        amplitude = np.max(frames)
        frequency = np.fft.rfftfreq(len(frames), d=1.0/RATE)
        spectrum = np.abs(np.fft.rfft(frames))
        dominant_frequency = frequency[np.argmax(spectrum)]

        print("大きさ", amplitude)
        print("高さ", dominant_frequency)

        frames = []  # フレームをリセット
        frames_received = 0  # 取得したフレーム数をリセット

stream.stop_stream()
stream.close()
p.terminate()