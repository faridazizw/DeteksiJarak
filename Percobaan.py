import numpy as np
import cv2
import time
import tkinter
from PIL import Image, ImageTk
from math import sqrt

lower = np.array([5, 120, 255])
upper = np.array([35, 255, 255])

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


root = tkinter.Tk()
root.title("Deteksi Jarak")
L1 = tkinter.Label(root, bg="red")
L1.grid(row=0, column=0, sticky='W')

L2 = tkinter.Label(root, bg="red")
L2.grid(row=0, column=1, sticky='N')

# L3 = tkinter.Label(root, text="ssadsfasdfas")
# L3.grid(row=1, column=0, sticky='S')

# Load Yolo
# net = cv2.dnn.readNet("weight/yolov3-tiny.weights", "cfg/yolov3-tiny.cfg")
net = cv2.dnn.readNet("model/8yolov3_training_best58,45.weights", "cfg/yolov3_training.cfg")
classes = []
with open("classes.txt", "r") as f:
    classes = [line.strip() for line in f.readlines()]
layer_names = net.getLayerNames()
output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
colors = np.random.uniform(0, 255, size=(len(classes), 3))  # Generate Random Color

# Load Videoq
cap = cv2.VideoCapture("video/pedestrian2.mp4")  # 0 -> Webcam; "/path"
font = cv2.FONT_HERSHEY_SIMPLEX

timeframe = time.time()
frame_id = 0

while True:
    _, frame = cap.read()
    frame_id += 1
    height, width, channels = frame.shape

    cv2.circle(frame, (400, 130), 5, (0, 0, 255), -1)
    cv2.circle(frame, (700, 170), 5, (0, 0, 255), -1)
    cv2.circle(frame, (10, 320), 5, (0, 0, 255), -1)
    cv2.circle(frame, (350, 470), 5, (0, 0, 255), -1)

    pts1 = np.float32([[400, 130], [700, 170], [10, 320], [350, 470]])
    pts2 = np.float32([[0, 0], [350, 0], [0, 500], [300, 500]])
    matrix = cv2.getPerspectiveTransform(pts1, pts2)

    # Detecting objects
    blob = cv2.dnn.blobFromImage(frame, 0.00392, (320, 320), (0, 0, 0), True, crop=False)

    net.setInput(blob)
    outs = net.forward(output_layers)

    # Showing informations on the screen
    class_ids = []
    confidences = []
    boxes = []
    for out in outs:
        for detection in out:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if confidence > 0.3:  # Confidence Level -> Accuracy
                # Object detected
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)

                # Rectangle coordinates
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)

                boxes.append([x, y, w, h])
                confidences.append(float(confidence))
                class_ids.append(class_id)

    indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)

    for i in range(len(boxes)):
        if i in indexes:
            x, y, w, h = boxes[i]

            label = str(classes[class_ids[i]])
            confidence = confidences[i]
            # color = colors[i]
            color = (255, 255, 0)
            cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)
            cv2.putText(frame, label, (x, y + 30), font, 1, color, 2)
            cv2.putText(frame, label + " " + str(round(confidence, 2)), (x, y + 30), font, 1, color, 2)
            cv2.circle(frame, (x + int(w / 2), y + h), 5, (0, 255, 255), -1)

    elapsed_time = time.time() - timeframe
    fps = frame_id / elapsed_time
    cv2.putText(frame, str(round(fps, 2)), (10, 50), font, 2, (255, 255, 255), 2)  # FPS Value
    cv2.putText(frame, "FPS", (220, 50), font, 2, (255, 255, 255), 2)  # FPS Label

    result = cv2.warpPerspective(frame, matrix, (350, 500))

    # perhitungan jarak
    image = cv2.cvtColor(result, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(image, lower, upper)

    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    kernelOp = np.ones((3, 3), np.uint8)

    poin = []
    jarakMin = 200

    if len(contours) != 0:
        for contours in contours:

            if cv2.contourArea(contours) > 10:
                x, y, w, h = cv2.boundingRect(contours)
                # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                cv2.circle(result, (x + int(w / 2), y + int(h / 2)), 5, (255, 255, 255), -1)
                cv2.circle(result, (x + int(w / 2), y + int(h / 2)), int(jarakMin/2), (0, 255, 255), 1)

                poin.append([x + int(w / 2), y + int(h / 2)])

    if len(poin) >= 2:
        x1 = poin[0][0]
        y1 = poin[0][1]

        x2 = poin[1][0]
        y2 = poin[1][1]

        # jarak x1 - x2
        if x1 > x2:
            jarak12 = hitungJarak(x1, x2, y1, y2)
            # cv2.putText(img, str(int(jarak12)), (int(jarak12 / 2), int(jarak12)), font, 1, color, 2)
        elif x2 > x1:
            jarak12 = hitungJarak(x2, x1, y2, y1)
            # cv2.putText(img, str(int(jarak12)), (int(jarak12 / 2), int(jarak12 / 2)), font, 1, color, 2)

        if int(jarak12) < jarakMin:
            cv2.line(result, (x1, y1), (x2, y2), (0, 0, 255), 3)
        else:
            cv2.line(result, (x1, y1), (x2, y2), (255, 0, 0), 3)

        # jarak x1 - x3 && x2 - x3
        if len(poin) >= 3:
            x3 = poin[2][0]
            y3 = poin[2][1]

            if x1 > x3:
                jarak13 = hitungJarak(x1, x3, y1, y3)
            elif x3 > x1:
                jarak13 = hitungJarak(x3, x1, y3, y1)
            if x2 > x3:
                jarak23 = hitungJarak(x2, x3, y2, y3)
            elif x3 > x2:
                jarak23 = hitungJarak(x3, x2, y3, y2)

            if int(jarak13) < jarakMin:
                cv2.line(result, (x1, y1), (x3, y3), (0, 0, 255), 3)
            else:
                cv2.line(result, (x1, y1), (x3, y3), (255, 0, 0), 3)
            if int(jarak23) < jarakMin:
                cv2.line(result, (x2, y2), (x3, y3), (0, 0, 255), 3)
            else:
                cv2.line(result, (x2, y2), (x3, y3), (255, 0, 0), 3)

            # jarak x1 - x4 && x2 - x4 && x3 - x4
            if len(poin) >= 4:
                x4 = poin[3][0]
                y4 = poin[3][1]

                if x1 > x4:
                    jarak14 = hitungJarak(x1, x4, y1, y4)
                elif x4 > x1:
                    jarak14 = hitungJarak(x4, x1, y4, y1)
                if x2 > x4:
                    jarak24 = hitungJarak(x2, x4, y2, y4)
                elif x4 > x2:
                    jarak24 = hitungJarak(x4, x2, y4, y2)
                if x3 > x4:
                    jarak34 = hitungJarak(x3, x4, y3, y4)
                elif x4 > x3:
                    jarak34 = hitungJarak(x4, x3, y4, y3)

                if int(jarak14) < jarakMin:
                    cv2.line(result, (x1, y1), (x4, y4), (0, 0, 255), 3)
                else:
                    cv2.line(result, (x1, y1), (x4, y4), (255, 0, 0), 3)
                if int(jarak24) < jarakMin:
                    cv2.line(result, (x2, y2), (x4, y4), (0, 0, 255), 3)
                else:
                    cv2.line(result, (x2, y2), (x4, y4), (255, 0, 0), 3)
                if int(jarak34) < jarakMin:
                    cv2.line(result, (x3, y3), (x4, y4), (0, 0, 255), 3)
                else:
                    cv2.line(result, (x3, y3), (x4, y4), (255, 0, 0), 3)

            else:
                jarak14 = 0
                jarak24 = 0
                jarak34 = 0

        else:
            jarak13 = 0
            jarak23 = 0
    else:
        jarak12 = 0

    cv2.putText(result, "jarak 1 & 2 : " + str(int(jarak12)), (30, 50), font, 1, color, 2)
    cv2.putText(result, "jarak 1 & 3 : " + str(int(jarak13)), (30, 80), font, 1, color, 2)
    cv2.putText(result, "jarak 1 & 4 : " + str(int(jarak14)), (30, 110), font, 1, color, 2)
    cv2.putText(result, "jarak 2 & 3 : " + str(int(jarak23)), (30, 140), font, 1, color, 2)
    cv2.putText(result, "jarak 2 & 4 : " + str(int(jarak24)), (30, 170), font, 1, color, 2)
    cv2.putText(result, "jarak 3 & 4 : " + str(int(jarak34)), (30, 200), font, 1, color, 2)

    img1 = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame = ImageTk.PhotoImage(Image.fromarray(img1))

    img2 = cv2.cvtColor(result, cv2.COLOR_BGR2RGB)
    persp = ImageTk.PhotoImage(Image.fromarray(img2))

    L1['image'] = frame
    L2['image'] = persp

    root.update()

    key = cv2.waitKey(1)
    if key == 27:  # Escape
        break

cap.release()
cv2.destroyAllWindows()
