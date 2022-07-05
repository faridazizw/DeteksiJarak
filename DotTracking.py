import cv2
import numpy as np
from math import sqrt

lower = np.array([5, 120, 255])
upper = np.array([35, 255, 255])

video = cv2.VideoCapture("video/pedestrian3.mp4")

font = cv2.FONT_HERSHEY_SIMPLEX
color = (255, 0, 0)

def hitungJarak(x1,x2,y1,y2):
    return sqrt((x2-x1)**2 + (y2-y1)**2)

while True:
    success, img = video.read()
    image = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    kernelOp = np.ones((3, 3), np.uint8)

    poin = []

    if len(contours) != 0:
        for contours in contours:

            if cv2.contourArea(contours) > 50:
                x, y, w, h = cv2.boundingRect(contours)
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.circle(img, (x + int(w / 2), y + int(h / 2)), 5, (255, 255, 255), -1)
                cv2.circle(img, (x + int(w / 2), y + int(h / 2)), 100, (0, 255, 255), 1)

                # cv2.putText(img, str(x) + "," + str(y), (x, y + 30), font, 1, color, 2)

                poin.append([x, y])

                # cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

    if len(poin) >= 2:
        x1 = poin[0][0]
        y1 = poin[0][1]

        x2 = poin[1][0]
        y2 = poin[1][1]

        jarak = 0

        if x1 > x2:
            jarak = hitungJarak(x1,x2,y1,y2)
            cv2.putText(img, str(jarak), (int(jarak/2), int(jarak)), font, 1, color, 2)
        elif x2 > x1:
            jarak = hitungJarak(x2,x1,y2,y1)
            cv2.putText(img, str(jarak), (int(jarak/2), int(jarak/2)), font, 1, color, 2)

        cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

        if len(poin) >= 3:
            x3 = poin[2][0]
            y3 = poin[2][1]

            cv2.line(img, (x1, y1), (x3, y3), (255, 0, 0), 3)
            cv2.line(img, (x2, y2), (x3, y3), (255, 0, 0), 3)

            if len(poin) >= 4:
                x4 = poin[3][0]
                y4 = poin[3][1]

                cv2.line(img, (x1, y1), (x4, y4), (255, 0, 0), 3)
                cv2.line(img, (x2, y2), (x4, y4), (255, 0, 0), 3)
                cv2.line(img, (x3, y3), (x4, y4), (255, 0, 0), 3)

        print(jarak)

    cv2.imshow("mask", mask)
    cv2.imshow("video", img)

    cv2.waitKey(27)
