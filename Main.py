import tkinter as tk
import cv2
import numpy as np
# import webcolors
import color
import voice_recognition
import threading
from PIL import Image, ImageTk
import os
import random
import csv
from googletrans import Translator
import re
import time


class users:
    def __init__(self):
        users_list = []

class user:
    def __init__(self):
        self.name = None
        self.birthday = None
        self.feeling = None
        self.painting_taste = None
        self.painting_style = None
        self.amplitude = None
        self.dominant_frequency = None
        self.color = None

    def get(self):
        print(vars(self))

    def save_to_csv(self, filename):
        with open(filename, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([
                self.name,
                self.birthday,
                self.painting_style,
                self.color
            ])

    def save_to_txt(self, filename):
        text = "–prompt “"
        with open(filename, "w") as file:
            text += self.feeling + ","
            text += self.painting_taste + ","
            text += self.amplitude + ","
            text += self.dominant_frequency + ","
            # text += "“–negative_prompt “(EasyNegative:1.2), cropped, error” –width 400 –height 400 –batch_size 2"
            file.write(text)

# 画面遷移
def show_screen_screen_register():
    screen_register.pack()
    screen_question.pack_forget()
    frame.pack_forget()
    clothing.pack_forget()
    screen_voice.pack_forget()
    fin.pack_forget()

def to_question():
    if tomoki.name and tomoki.birthday is not None:
        screen_register.pack_forget()
        screen_question.pack()
        message.config(text="") 
    else:
        message.config(text="未入力の項目があります")

def to_painting_style():
    if tomoki.feeling and tomoki.painting_taste is not None and not tomoki.painting_taste == "":
        screen_question.pack_forget()
        frame.pack()
        message.config(text="")
    else:
        message.config(text="未入力の項目があります") 

def to_voice_recognition():
        frame.pack_forget()
        screen_voice.pack()
        message.config(text="")

def to_clothing_recognition():
        screen_voice.pack_forget()
        clothing.pack()
        message.config(text="")

def to_fin():
        clothing.pack_forget()
        fin.pack()
        message.config(text="")

def to_start():
        fin.pack_forget()
        screen_register.pack()
        message.config(text="")
# 入力処理
translator = Translator()

def send_name():
    name = text_name.get()
    name_label.config(text=name)
    tomoki.name = translator.translate(name).text
    print(tomoki.name)

def send_birth():
    birth = text_birth.get()
    if validate_date_of_birth(birth):
        birth_label.config(text=birth)
        tomoki.birthday = birth
        print(tomoki.birthday)
    else:
        birth_label.config(text="入力が正しくありません")
    
def send_feeling():
    feeling = box_feeling.get()
    box_feeling.config(text=feeling)
    tomoki.feeling = translator.translate(feeling).text
    print(tomoki.feeling)

def send_painting_taste():
    painting_taste = text_painting_taste.get()
    painting_taste_label.config(text=painting_taste)
    tomoki.painting_taste = translator.translate(painting_taste).text
    print(tomoki.painting_taste)

def validate_date_of_birth(date_string):
    # 生年月日の正しい形式（YYYY-MM-DD）を持つかどうかをチェックする正規表現パターン
    pattern = r'^\d{4}-\d{2}-\d{2}$'
    if not re.match(pattern, date_string):
        return False
    year, month, day = date_string.split('-')

    # 年、月、日が有効な範囲にあるかどうかをチェック
    if int(year) < 1900 or int(year) > 2023:
        return False
    if int(month) < 1 or int(month) > 12:
        return False
    if int(day) < 1 or int(day) > 31:
        return False
    return True

def sound_conversion(amplitude , dominant_frequency):
    if amplitude > 200:
        amplitude_str = "sunshine"
    elif amplitude > 180:
        amplitude_str = "the sun"
    elif amplitude > 160:
        amplitude_str = "cloud"
    elif amplitude > 140:
        amplitude_str = "rain"
    elif amplitude > 130:
        amplitude_str = "snow"
    else:
        amplitude_str = "fog"

    if dominant_frequency < 20:
        dominant_frequency_str = "Darkness"
    elif dominant_frequency < 50:
        dominant_frequency_str = "Dimness"
    elif dominant_frequency < 80:
        dominant_frequency_str = "Dim light"
    elif dominant_frequency < 100:
        dominant_frequency_str = "Soft light"
    elif dominant_frequency < 200:
        dominant_frequency_str = "Bright light"
    elif dominant_frequency < 300:
        dominant_frequency_str = "Blinding light"
    else:
        dominant_frequency_str = "Extreme brightness"

    return amplitude_str , dominant_frequency_str

#///////////////////////////////////////////////////////
#画風処理

def show_image(image_path):
    global selected_image

    image = Image.open(image_path)

    thumbnail_size = (200, 200)
    image.thumbnail(thumbnail_size, Image.LANCZOS)

    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(frame, image=image_tk)
    image_label.image = image_tk
    image_label.pack(padx=10, pady=10)

    def on_image_click(path):
        global selected_image
        selected_image = path
        print(selected_image)
        tomoki.painting_style = selected_image
        to_voice_recognition()
        voice_start()

    image_label.bind("<Button-1>", lambda event, path=image_path: on_image_click(path))

def show_random_images():
    image_files = os.listdir(image_folder)
    random_images = random.sample(image_files, 1)
    for widget in frame.winfo_children():
        widget.destroy()

    for image_file in random_images:
        image_path = os.path.join(image_folder, image_file)
        show_image(image_path)

def update_images():
    show_random_images()
    update_button = tk.Button(frame, text="更新", command=update_images);update_button.pack(side="bottom", pady=10)

#///////////////////////////////////////////////////////
#音声処理

def voice_start():
    thread1 = threading.Thread(target=run_voice_recognition)
    thread1.start()

def run_voice_recognition():
    global voice
    voice = voice_recognition.voice()
    voice.recognition()

def stop_voice_recognition():
    global voice
    if voice.amplitude == 0 and voice.dominant_frequency == 0:
        message.config(text="まだ測定できていません")
    else:
        tomoki.amplitude , tomoki.dominant_frequency = sound_conversion(voice.amplitude , voice.dominant_frequency)
        voice.Flag = False
        to_clothing_recognition()

#///////////////////////////////////////////////////////
#服装処理

class ClothRecognition:
    def __init__(self):
        self.cascade_path = '/Users/apple/project/recognition/haarcascade/opencv/data/haarcascades/haarcascade_fullbody.xml'
        self.flag = True

    def start_recognition(self):
        cap = cv2.VideoCapture(1)
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
                    tomoki.color = closest_color
                except:
                    a = 0
                cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            cv2.imshow('Frame', frame)
            cv2.waitKey(10)
            clothing.after(10, process_frame)

        process_frame()

    def stop_recognition(self):
        self.flag = False

def start_button_click():
    cloth_recognition.start_recognition()

def stop_button_click():
    if tomoki.color is None:
        message.config(text="まだ測定できていません")
    else:
        cloth_recognition.stop_recognition()
        to_fin()
        print("fin")

#///////////////////////////////////////////////////////
#ユーザの要素をプロンプトへ

def send_attr():
    # to_start()
    tomoki.save_to_txt("./data/text/"  + tomoki.name + ".txt")
    tomoki.save_to_csv("./data/csv/chatgpt.csv")

#///////////////////////////////////////////////////////
#デバック用
def print_thread_count():
    count = threading.active_count()
    print("現在のスレッド数:", count)


#///////////////////////////////////////////////////////
#main処理

tomoki = user()

root = tk.Tk()
root.title("OdagiriPro_Sys")
root.geometry("800x400")
root.attributes('-fullscreen', True)
# root.bind('',lambda e: root.destroy())
# User_information = tk.Button(root, text="登録情報", command=tomoki.get);User_information.pack(side=tk.RIGHT)
# test1 = tk.Button(root, text="スレッド数", command=print_thread_count);test1.pack(side=tk.RIGHT)
message = tk.Label(root, text="");message.pack(side = tk.BOTTOM)
#///////////////////////////////////////////////////////
# 個人情報のフレーム
screen_register = tk.Frame(root);screen_register.pack()

label_register = tk.Label(screen_register, text="ユーザ登録");label_register.pack()


# 名前
label_name = tk.Label(screen_register, text="名前");label_name.pack()
text_name = tk.Entry(screen_register ,textvariable=tk.StringVar(value=''));text_name.pack()
button_name = tk.Button(screen_register, text="確定", command=send_name);button_name.pack()
name_label = tk.Label(screen_register, text="");name_label.pack()

# 生年月日
label_birth = tk.Label(screen_register, text="誕生日");label_birth.pack()
text_birth = tk.Entry(screen_register,textvariable = tk.StringVar(value=''));text_birth.pack()
button_birth = tk.Button(screen_register, text="確定", command=send_birth);button_birth.pack()
label_ex = tk.Label(screen_register, text="例：2002-01-01");label_ex.pack()
birth_label = tk.Label(screen_register, text="");birth_label.pack()

# message = tk.Label(screen_register, text="");message.pack()
button_a = tk.Button(screen_register, text="質問コーナーへ", command=to_question);button_a.pack()



#///////////////////////////////////////////////////////
#質問のフレーム
screen_question = tk.Frame(root);screen_question.pack()
label_b = tk.Label(screen_question, text="質問");label_b.pack()
# 気分
type_of_mood = ["楽しい","悲しい","ワクワク"]
label_feeling = tk.Label(screen_question, text="気分");label_feeling.pack()
box_feeling = tk.Spinbox(screen_question, state="readonly", values=type_of_mood , command=send_feeling);box_feeling.pack()

# 絵の好み
label_painting_taste = tk.Label(screen_question, text="絵の好み");label_painting_taste.pack()
text_painting_taste = tk.Entry(screen_question,textvariable = tk.StringVar(value=''));text_painting_taste.pack()
button_painting_taste = tk.Button(screen_question, text="確定", command=send_painting_taste);button_painting_taste.pack()
painting_taste_label = tk.Label(screen_question, text="");painting_taste_label.pack()

# message = tk.Label(screen_question, text="");message.pack()
button_a = tk.Button(screen_question, text="画風コーナーへ", command=to_painting_style);button_a.pack()

#///////////////////////////////////////////////////////
#画風のフレーム
image_folder = "./picture"
frame = tk.Frame(root)
update_images()
frame.pack()

#///////////////////////////////////////////////////////
#音声認識のフレーム

screen_voice = tk.Frame(root);screen_voice.pack()
label_b = tk.Label(screen_voice, text="音声認識中");label_b.pack()
label_c = tk.Label(screen_voice, text="10秒間計測します。");label_c.pack()
label_d = tk.Label(screen_voice, text="ポスターどうでしたか？");label_d.pack()
# voice_start_b = tk.Button(screen_voice, text="起動", command=voice_start);voice_start_b.pack() # 前フレームで実行
voice_stop = tk.Button(screen_voice, text="終了", command=stop_voice_recognition);voice_stop.pack()

# message = tk.Label(screen_voice, text="");message.pack()
#///////////////////////////////////////////////////////
#服装認識のフレーム

clothing = tk.Frame(root);clothing.pack()
label_b = tk.Label(clothing, text="画像認識");label_b.pack()

cloth_recognition = ClothRecognition()

start_button = tk.Button(clothing, text="開始", command=start_button_click);start_button.pack()
stop_button = tk.Button(clothing, text="終了", command=stop_button_click);stop_button.pack()


#///////////////////////////////////////////////////////
#結果のフレーム
fin = tk.Frame(root);fin.pack()

label_b = tk.Label(fin, text="終了");label_b.pack()

send = tk.Button(fin, text="送信", command=send_attr);send.pack()

#///////////////////////////////////////////////////////
#main start
show_screen_screen_register()
root.mainloop()