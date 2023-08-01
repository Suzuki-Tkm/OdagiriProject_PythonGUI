import pyaudio
import numpy as np

# マイクから音声データを取得するコールバック関数
def audio_callback(in_data, frame_count, time_info, status):
    audio_data = np.frombuffer(in_data, dtype=np.float32)
    
    # 音声データの処理（ここでは最大振幅を求める）
    amplitude = np.max(np.abs(audio_data))
    
    # 音声の高さ（ピッチ）を求める場合は、FFTなどの信号処理手法を利用する必要があります
    
    # 音声のスピード（音の変動速度）を求める場合は、フレーム間の差分を計算するなどの手法を利用します
    
    # 数値化した結果を表示
    print('Amplitude:', amplitude)
    
    # 処理した音声データを返す
    return (audio_data, pyaudio.paContinue)

# PyAudioの初期化
p = pyaudio.PyAudio()

# マイクから音声データを取得するストリームを開く
stream = p.open(format=pyaudio.paFloat32,
                channels=1,
                rate=44100,
                input=True,
                frames_per_buffer=1024,
                stream_callback=audio_callback)

# 音声データの取得と処理を開始
stream.start_stream()

# プログラムが終了されるまで待機
while stream.is_active():
    pass

# ストリームを停止して終了
stream.stop_stream()
stream.close()
p.terminate()
