import cv2
import numpy as np
import webcolors
import color

cascade_path = '/Users/apple/project/recognition/haarcascade/opencv/data/haarcascades/haarcascade_fullbody.xml'
cap = cv2.VideoCapture(1)
cascade = cv2.CascadeClassifier(cascade_path)

while True:
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
            print((int(most_common_color[0]), int(most_common_color[1]),int(most_common_color[2])))
            r , g , b = int(most_common_color[0]), int(most_common_color[1]),int(most_common_color[2])
            closest_color = color.get_approximate_color_name((r, g, b))
            print(closest_color)
        except:
            a = 0
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
    cv2.imshow('Frame', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release() 
cv2.destroyAllWindows()