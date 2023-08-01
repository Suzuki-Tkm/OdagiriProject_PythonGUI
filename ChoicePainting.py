import tkinter as tk
from PIL import Image, ImageTk
import os
import random

image_folder = "./picture"

window = tk.Tk()

frame = tk.Frame(window)
frame.pack()

selected_image = ""

def show_image(image_path):
    global selected_image

    image = Image.open(image_path)

    thumbnail_size = (200, 200)
    image.thumbnail(thumbnail_size, Image.ANTIALIAS)

    image_tk = ImageTk.PhotoImage(image)
    image_label = tk.Label(frame, image=image_tk)
    image_label.image = image_tk
    image_label.pack(padx=10, pady=10)

    def on_image_click(path):
        global selected_image
        selected_image = path
        window.destroy()

    image_label.bind("<Button-1>", lambda event, path=image_path: on_image_click(path))

def show_random_images():
    image_files = os.listdir(image_folder)
    random_images = random.sample(image_files, 3)
    for widget in frame.winfo_children():
        widget.destroy()

    for image_file in random_images:
        image_path = os.path.join(image_folder, image_file)
        show_image(image_path)

def update_images():
    show_random_images()

update_button = tk.Button(window, text="更新", command=update_images)
update_button.pack(pady=10)

show_random_images()

window.mainloop()

print("選択された画像のパス:", selected_image)