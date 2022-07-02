import cv2
import numpy as np

lower = np.array([5, 120, 255])
upper = np.array([35, 255, 255])

video = cv2.VideoCapture("video/pedestrian3.mov")

while True:
    success, img = video.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if len(contours) != 0:
        for contours in contours:
            if cv2.contourArea(contours) > 50:
                x, y, w, h = cv2.boundingRect(contours)
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.circle(img, (x + int(w / 2), y + int(h/2)), 5, (255, 255, 255), -1)
                cv2.circle(img, (x + int(w / 2), y + int(h / 2)), 100, (0, 255, 255), 1)

    cv2.imshow("mask", mask)
    cv2.imshow("video", img)

    cv2.waitKey(27)