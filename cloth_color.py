import cv2
import numpy as np

class cloth_color:
    def __init__(self):
        self.image = cv2.imread('/Users/apple/Downloads/DSC_0614.JPG')
        self.cascade_path = '/Users/apple/project/recognition/haarcascade/opencv/data/haarcascades/haarcascade_fullbody.xml'
        self.cascade = cv2.CascadeClassifier(self.cascade_path)
        self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.bodies = self.cascade.detectMultiScale(self.gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
        self.flag = True

    def recognition(self):
        for (x, y, w, h) in self.bodies:
            if not self.flag: break
            cv2.rectangle(self.image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi = self.image[y:y + h, x:x + w]

    # 服の色抽出
            blurred = cv2.GaussianBlur(roi, (5, 5), 0)
            hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
            lower_color = np.array([0, 50, 50])
            upper_color = np.array([10, 255, 255])
            mask = cv2.inRange(hsv, lower_color, upper_color)
            color = cv2.bitwise_and(roi, roi, mask=mask)

    # RGB形式に変換
            color_rgb = cv2.cvtColor(color, cv2.COLOR_BGR2RGB)

    # 服の色を抽出してテキストで表示
            avg_color = np.average(color_rgb.reshape(-1, 3), axis=0)
            avg_color = avg_color.astype(int)
            color_text = f"R: {avg_color[0]}, G: {avg_color[1]}, B: {avg_color[2]}"
            print("服の色:", color_text)

# 人物領域を表示
        cv2.imshow("Detection", self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def stop(self):
        self.flag = False

test = cloth_color()
test.recognition()