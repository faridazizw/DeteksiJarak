import cv2
import numpy as np
from math import sqrt


class HitungJarak():
    lower = np.array([5, 120, 255])
    upper = np.array([35, 255, 255])

    video = cv2.VideoCapture("video/pedestrian3.mp4")

    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 0, 0)

    jarak12 = 0
    jarak13 = 0
    jarak14 = 0
    jarak23 = 0
    jarak24 = 0
    jarak34 = 0

    def hitungJarak(x1, x2, y1, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

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
                    cv2.circle(img, (x + int(w / 2), y + int(h / 2)), 200, (0, 255, 255), 1)

                    # cv2.putText(img, str(x) + "," + str(y), (x, y + 30), font, 1, color, 2)

                    poin.append([x + int(w / 2), y + int(h / 2)])

                    # cv2.line(img,(x1,y1),(x2,y2),(255,0,0),3)

        if len(poin) >= 2:
            x1 = poin[0][0]
            y1 = poin[0][1]

            x2 = poin[1][0]
            y2 = poin[1][1]

            # jarak x1 - x2
            if x2 > x1:
                jarak12 = hitungJarak(x1, x2, y1, y2)
                # cv2.putText(img, str(int(jarak12)), (int(jarak12 / 2), int(jarak12)), font, 1, color, 2)
            elif x1 > x2:
                jarak12 = hitungJarak(x2, x1, y2, y1)
                # cv2.putText(img, str(int(jarak12)), (int(jarak12 / 2), int(jarak12 / 2)), font, 1, color, 2)

            if int(jarak12) < 400:
                cv2.line(img, (x1, y1), (x2, y2), (0, 0, 255), 3)
            else:
                cv2.line(img, (x1, y1), (x2, y2), (255, 0, 0), 3)

            # jarak x1 - x3 && x2 - x3
            if len(poin) >= 3:
                x3 = poin[2][0]
                y3 = poin[2][1]

                if x3 > x1:
                    jarak13 = hitungJarak(x1, x3, y1, y3)
                elif x1 > x3:
                    jarak13 = hitungJarak(x3, x1, y3, y1)
                if x3 > x2:
                    jarak23 = hitungJarak(x2, x3, y2, y3)
                elif x2 > x3:
                    jarak23 = hitungJarak(x3, x2, y3, y2)

                if int(jarak13) < 400:
                    cv2.line(img, (x1, y1), (x3, y3), (0, 0, 255), 3)
                else:
                    cv2.line(img, (x1, y1), (x3, y3), (255, 0, 0), 3)
                if int(jarak23) < 400:
                    cv2.line(img, (x2, y2), (x3, y3), (0, 0, 255), 3)
                else:
                    cv2.line(img, (x2, y2), (x3, y3), (255, 0, 0), 3)

                # jarak x1 - x4 && x2 - x4 && x3 - x4
                if len(poin) >= 4:
                    x4 = poin[3][0]
                    y4 = poin[3][1]

                    if x4 > x1:
                        jarak14 = hitungJarak(x1, x4, y1, y4)
                    elif x1 > x4:
                        jarak14 = hitungJarak(x4, x1, y4, y1)
                    if x4 > x2:
                        jarak24 = hitungJarak(x2, x4, y2, y4)
                    elif x2 > x4:
                        jarak24 = hitungJarak(x4, x2, y4, y2)
                    if x4 > x3:
                        jarak34 = hitungJarak(x3, x4, y3, y4)
                    elif x3 > x4:
                        jarak34 = hitungJarak(x4, x3, y4, y3)

                    if int(jarak14) < 400:
                        cv2.line(img, (x1, y1), (x4, y4), (0, 0, 255), 3)
                    else:
                        cv2.line(img, (x1, y1), (x4, y4), (255, 0, 0), 3)
                    if int(jarak24) < 400:
                        cv2.line(img, (x2, y2), (x4, y4), (0, 0, 255), 3)
                    else:
                        cv2.line(img, (x2, y2), (x4, y4), (255, 0, 0), 3)
                    if int(jarak34) < 400:
                        cv2.line(img, (x3, y3), (x4, y4), (0, 0, 255), 3)
                    else:
                        cv2.line(img, (x3, y3), (x4, y4), (255, 0, 0), 3)

                else:
                    jarak14 = 0
                    jarak24 = 0
                    jarak34 = 0

            else:
                jarak13 = 0
                jarak23 = 0
        else:
            jarak12 = 0

        cv2.putText(img, "jarak 1 & 2 : " + str(int(jarak12)), (30, 50), font, 1, color, 2)
        cv2.putText(img, "jarak 1 & 3 : " + str(int(jarak13)), (30, 80), font, 1, color, 2)
        cv2.putText(img, "jarak 1 & 4 : " + str(int(jarak14)), (30, 110), font, 1, color, 2)
        cv2.putText(img, "jarak 2 & 3 : " + str(int(jarak23)), (30, 140), font, 1, color, 2)
        cv2.putText(img, "jarak 2 & 4 : " + str(int(jarak24)), (30, 170), font, 1, color, 2)
        cv2.putText(img, "jarak 3 & 4 : " + str(int(jarak34)), (30, 200), font, 1, color, 2)

        cv2.imshow("mask", mask)
        cv2.imshow("video", img)

        cv2.waitKey(27)


if __name__ == '__main__':
    HitungJarak()
