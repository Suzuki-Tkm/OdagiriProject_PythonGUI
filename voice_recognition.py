import pyaudio
import numpy as np



class voice():
    def __init__(self):
        self.CHUNK = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 44100
        self.DURATION = 10  # 10秒間の平均値を取得する
        self.Flag = True
        self.dominant_frequency = 0
        self.amplitude = 0

    def recognition(self):
        p = pyaudio.PyAudio()

        stream = p.open(format=self.FORMAT,channels=self.CHANNELS,rate=self.RATE,input=True,frames_per_buffer=self.CHUNK)

        frames = []  # データのフレームを保存するリスト
        duration_frames = self.RATE * self.DURATION  # 10秒間のフレーム数
        frames_received = 0  # 取得したフレーム数のカウンタ

        while self.Flag:
            data = np.frombuffer(stream.read(self.CHUNK), dtype=np.int16)
            frames.append(data)
            frames_received += len(data)

            if frames_received >= duration_frames:
                frames = np.concatenate(frames)[:duration_frames]  # 必要なフレーム数だけ取得
                self.amplitude = np.max(frames)
                frequency = np.fft.rfftfreq(len(frames), d=1.0/self.RATE)
                spectrum = np.abs(np.fft.rfft(frames))
                self.dominant_frequency = frequency[np.argmax(spectrum)]
                print("大きさ", self.amplitude)
                print("高さ", self.dominant_frequency)

                frames = []  # フレームをリセット
                frames_received = 0  # 取得したフレーム数をリセット
        print("fin")
        stream.stop_stream()
        stream.close()
        p.terminate()

# v = voice()
# v.recognition()