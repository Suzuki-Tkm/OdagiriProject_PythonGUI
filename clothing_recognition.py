import tkinter as tk
import cv2
import numpy as np
import webcolors
import color

class ClothRecognition:
    def __init__(self):
        self.cascade_path = '/Users/apple/project/recognition/haarcascade/opencv/data/haarcascades/haarcascade_fullbody.xml'
        self.flag = True

    def start_recognition(self):
        cap = cv2.VideoCapture(0)
        cascade = cv2.CascadeClassifier(self.cascade_path)

        def process_frame():
            if not self.flag:
                cap.release()
                cv2.destroyAllWindows()
                return
            ret, frame = cap.read()
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            bodies = cascade.detectMultiScale(gray)

            for (x, y, w, h) in bodies:
                body_roi = frame[y:y+h, x:x+w]
                resized_roi = cv2.resize(body_roi, (100, 100))
                hsv_roi = cv2.cvtColor(resized_roi, cv2.COLOR_BGR2HSV)
                flattened_roi = hsv_roi.reshape(-1, 3)
                colors, counts = np.unique(flattened_roi, axis=0, return_counts=True)
                most_common_color = colors[np.argmax(counts)]
                try:
                    print((int(most_common_color[0]), int(most_common_color[1]), int(most_common_color[2])))
                    r, g, b = int(most_common_color[0]), int(most_common_color[1]), int(most_common_color[2])
                    closest_color = color.get_approximate_color_name((r, g, b))
                    print(closest_color)
                except:
                    a = 0
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Frame', frame)
            cv2.waitKey(1)
            root.after(10, process_frame)

        process_frame()

    def stop_recognition(self):
        self.flag = False

# Tkinterウィンドウを作成
root = tk.Tk()
root.title("Cloth Recognition")
root.geometry("400x400")

# ClothRecognitionオブジェクトを作成
cloth_recognition = ClothRecognition()

# 開始ボタンをクリックしたときの処理
def start_button_click():
    cloth_recognition.start_recognition()

# 終了ボタンをクリックしたときの処理
def stop_button_click():
    cloth_recognition.stop_recognition()

