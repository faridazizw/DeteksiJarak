from doctest import master
from tkinter import messagebox
import tkinter
import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import *

import six
from PIL import ImageTk, Image

import time
from math import sqrt


class Video:

    def __init__(self):
        self.curdir = ""
        self.tempdir = ""
        self.cap = ""
        self.prevWindow = ""
        self.procWindow = ""
        self.jarakMin = "200"

    def btn_openFile(self):
        main_window.withdraw()

        self.curdir = os.getcwd()
        self.tempdir = filedialog.askopenfilename(parent=main_window, initialdir=self.curdir,
                                                  title='Plilih lokasi video', filetypes=[
                ("all video format", ".mp4"),
                ("all video format", ".flv"),
                ("all video format", ".avi"),
            ])

        ent1.insert(0, str(self.tempdir))

        main_window.deiconify()
        return self.tempdir

    def btn_mulai(self):
        if var_rb.get() == 1:
            path = ent1.get()
            if path == "":
                pc.msgBox2()
            else:
                main_window.withdraw()
                self.cap = cv2.VideoCapture(path)

                if (self.cap.isOpened() == False):
                    pc.msgBox3()
                    main_window.deiconify()
                else:
                    pc.openPrevWindow(self.cap)

        elif var_rb.get() == 2:
            path = ent2.get()
            if path == "":
                pc.msgBox2()
            elif isinstance(int(path), str):
                pc.msgBox3()
            else:
                main_window.withdraw()
                self.cap = cv2.VideoCapture(int(path))

                if (self.cap.isOpened() == False):
                    pc.msgBox3()
                    main_window.deiconify()
                else:
                    pc.openPrevWindow(self.cap)

    def clearValue(self):
        del coor[:]

    def msgBox1(self):
        messagebox.showerror("Kesalahan", "Jumlah koordinat tidak boleh lebih dari 4!")

    def msgBox2(self):
        messagebox.showerror("Kesalahan", "Video yang akan ditinjau tidak boleh kosong!")

    def msgBox3(self):
        messagebox.showerror("Kesalahan", "Kamera atau Video tidak ditemukan!")

    def msgBox4(self):
        messagebox.showerror("Kesalahan", "Jumlah koordinat tidak boleh kurang dari 4!")

    def displayCoordinates(self, event):
        if(len(coor)<4):
            coor.append([event.x, event.y])
            print(coor)
            print(len(coor))
        else:
            pc.msgBox1()

    def hide1(self):
        ent1.config(state='disabled')
        ent2.config(state='normal')
        lbl2.config(state='active')
        lbl3.config(state='active')
        btn_open.config(state='disabled')

    def hide2(self):
        ent1.config(state='normal')
        ent2.config(state='disabled')
        lbl2.config(state='disabled')
        lbl3.config(state='disabled')
        btn_open.config(state='active')

    def disable_event(self):
        pass

    def hitungJarak(self, x1, x2, y1, y2):
        return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

    def checkCoor(self):
        if(len(coor) < 4):
            pc.msgBox4()
            pc.openPrevWindow()

    def openPrevWindow(self, cap):
        self.prevWindow = Toplevel(master)

        self.prevWindow.title("Tinjau Video")
        self.prevWindow.grid_rowconfigure(0, weight=1)
        self.prevWindow.grid_columnconfigure(0, weight=1)

        frame1 = Frame(self.prevWindow)
        frame1.grid(row=0, column=0)

        lbltext1 = Label(frame1, text="Tentukan wilayah deteksi", font="Times 22 bold")
        lbltext1.grid(row=1)

        lblvideo = Label(frame1)
        lblvideo.grid(row=2)

        btnBack = Button(frame1, text="Kembali", command=lambda:[main_window.deiconify(), self.prevWindow.destroy()], width=20, font="bold")
        btnBack.grid(row=3, column=0, sticky=W, pady=15)

        btnClear = Button(frame1, text="Hapus", command=pc.clearValue, width=20, font="bold")
        btnClear.grid(row=3, column=0, pady=15)

        btnProses = Button(frame1, text="Proses", command=lambda:[pc.checkCoor(), pc.openProcessWindow(cap)], width=20, font="bold")
        btnProses.grid(row=3, column=0, sticky=E, pady=15)

        self.prevWindow.protocol("WM_DELETE_WINDOW", pc.disable_event)

        while True:
            _, frame = cap.read()

            if(len(coor) == 1):
                cv2.circle(frame, (int(coor[0][0]), int(coor[0][1])), 5, (0, 0, 255), -1)
            elif(len(coor) == 2):
                cv2.circle(frame, (int(coor[0][0]), int(coor[0][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[1][0]), int(coor[1][1])), 5, (0, 0, 255), -1)
                cv2.line(frame, (int(coor[0][0]), int(coor[0][1])), (int(coor[1][0]), int(coor[1][1])), (0, 0, 255), 3)
            elif(len(coor) == 3):
                cv2.circle(frame, (int(coor[0][0]), int(coor[0][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[1][0]), int(coor[1][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[2][0]), int(coor[2][1])), 5, (0, 0, 255), -1)
                cv2.line(frame, (int(coor[0][0]), int(coor[0][1])), (int(coor[1][0]), int(coor[1][1])), (0, 0, 255), 3)
                cv2.line(frame, (int(coor[1][0]), int(coor[1][1])), (int(coor[2][0]), int(coor[2][1])), (0, 0, 255), 3)
            elif(len(coor) == 4):
                cv2.circle(frame, (int(coor[0][0]), int(coor[0][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[1][0]), int(coor[1][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[2][0]), int(coor[2][1])), 5, (0, 0, 255), -1)
                cv2.circle(frame, (int(coor[3][0]), int(coor[3][1])), 5, (0, 0, 255), -1)
                cv2.line(frame, (int(coor[0][0]), int(coor[0][1])), (int(coor[1][0]), int(coor[1][1])), (0, 0, 255), 3)
                cv2.line(frame, (int(coor[1][0]), int(coor[1][1])), (int(coor[2][0]), int(coor[2][1])), (0, 0, 255), 3)
                cv2.line(frame, (int(coor[2][0]), int(coor[2][1])), (int(coor[3][0]), int(coor[3][1])), (0, 0, 255), 3)
                cv2.line(frame, (int(coor[3][0]), int(coor[3][1])), (int(coor[0][0]), int(coor[0][1])), (0, 0, 255), 3)

            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            framee = ImageTk.PhotoImage(Image.fromarray(cv2image))
            lblvideo['image'] = framee
            lblvideo.bind('<Button-1>', pc.displayCoordinates)

            cv2.waitKey(25)
            self.prevWindow.update()

    def updateJarak(self, entJarak, cap):
        self.jarakMin = entJarak
        self.procWindow.destroy()
        pc.openProcessWindow(cap)

    def openProcessWindow(self, cap):
        self.prevWindow.destroy()

        self.procWindow = Toplevel(master)

        lower = np.array([5, 120, 255])
        upper = np.array([35, 255, 255])

        color = (255, 0, 0)

        jarakMin1 = StringVar(self.procWindow, value=self.jarakMin)

        jarak12 = 0
        jarak13 = 0
        jarak14 = 0
        jarak23 = 0
        jarak24 = 0
        jarak34 = 0

        self.procWindow.grid_rowconfigure(0, weight=1)
        self.procWindow.grid_columnconfigure(0, weight=1)

        self.procWindow.title("Deteksi jarak antara manusia")
        L1 = tkinter.Label(self.procWindow)
        L1.grid(row=0, column=0, sticky='W')

        L2 = tkinter.Label(self.procWindow)
        L2.grid(row=0, column=1, sticky='N')

        btnBack = Button(self.procWindow, text="Kembali", command=lambda: [self.procWindow.destroy(), pc.btn_mulai()], width=20, font="bold")
        btnBack.grid(row=2, column=0, sticky=W, pady=15)

        entJarak = tkinter.Entry(self.procWindow, textvariable=jarakMin1)
        entJarak.grid(row=2, column=1, sticky='W')

        btnJarak = Button(self.procWindow, text="Update Jarak", command=lambda: [pc.updateJarak(entJarak.get(), cap)], width=20, font="bold")
        btnJarak.grid(row=2, column=1, sticky='E', pady=15)

        # lblJarak = tkinter.Label(procWindow, textvariable=jarakMin1)
        # lblJarak.grid(row=2, column=1, sticky='E')

        jarakMin = int(self.jarakMin)

        # Load Yolo
        net = cv2.dnn.readNet("model/8yolov3_training_best58,45.weights", "cfg/yolov3_training.cfg")
        classes = []
        with open("classes.txt", "r") as f:
            classes = [line.strip() for line in f.readlines()]
        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))  # Generate Random Color

        # Load Videoq
        font = cv2.FONT_HERSHEY_SIMPLEX

        timeframe = time.time()
        frame_id = 0

        while True:
            _, frame = cap.read()
            frame_id += 1
            height, width, channels = frame.shape

            cv2.circle(frame, (int(coor[0][0]), int(coor[0][1])), 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(coor[1][0]), int(coor[1][1])), 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(coor[2][0]), int(coor[2][1])), 5, (0, 0, 255), -1)
            cv2.circle(frame, (int(coor[3][0]), int(coor[3][1])), 5, (0, 0, 255), -1)
            cv2.line(frame, (int(coor[0][0]), int(coor[0][1])), (int(coor[1][0]), int(coor[1][1])), (0, 0, 255), 3)
            cv2.line(frame, (int(coor[1][0]), int(coor[1][1])), (int(coor[2][0]), int(coor[2][1])), (0, 0, 255), 3)
            cv2.line(frame, (int(coor[2][0]), int(coor[2][1])), (int(coor[3][0]), int(coor[3][1])), (0, 0, 255), 3)
            cv2.line(frame, (int(coor[3][0]), int(coor[3][1])), (int(coor[0][0]), int(coor[0][1])), (0, 0, 255), 3)

            pts1 = np.float32([[coor[0][0], coor[0][1]],
                               [coor[1][0], coor[1][1]],
                               [coor[2][0], coor[2][1]],
                               [coor[3][0], coor[3][1]]])
            pts2 = np.float32([[0, 0], [350, 0], [350, 500], [0, 500]])
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


            if len(contours) != 0:
                for contours in contours:

                    if cv2.contourArea(contours) > 10:
                        x, y, w, h = cv2.boundingRect(contours)
                        # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 3)
                        cv2.circle(result, (x + int(w / 2), y + int(h / 2)), 5, (255, 255, 255), -1)
                        cv2.circle(result, (x + int(w / 2), y + int(h / 2)), int(jarakMin / 2), (0, 255, 255), 1)

                        poin.append([x + int(w / 2), y + int(h / 2)])

            if len(poin) >= 2:
                x1 = poin[0][0]
                y1 = poin[0][1]

                x2 = poin[1][0]
                y2 = poin[1][1]

                # jarak x1 - x2
                if x1 > x2:
                    jarak12 = pc.hitungJarak(x1, x2, y1, y2)
                    # cv2.putText(img, str(int(jarak12)), (int(jarak12 / 2), int(jarak12)), font, 1, color, 2)
                elif x2 > x1:
                    jarak12 = pc.hitungJarak(x2, x1, y2, y1)
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
                        jarak13 = pc.hitungJarak(x1, x3, y1, y3)
                    elif x3 > x1:
                        jarak13 = pc.hitungJarak(x3, x1, y3, y1)
                    if x2 > x3:
                        jarak23 = pc.hitungJarak(x2, x3, y2, y3)
                    elif x3 > x2:
                        jarak23 = pc.hitungJarak(x3, x2, y3, y2)

                    if int(jarak13) < jarakMin:
                        cv2.line(result, (x1, y1), (x3, y3), (0, 0, 255), 3)
                    else:
                        cv2.line(result, (x1, y1), (x3, y3), (255, 0, 0), 3)
                    if int(jarak23) < jarakMin:
                        cv2.line(result, (x2, y2), (x3, y3), (0, 0, 255), 3)
                    else:
                        cv2.line(result, (x2, y2), (x3, y3), (255, 0, 0), 3)
                else:
                    jarak13 = 0
                    jarak23 = 0

                # jarak x1 - x4 && x2 - x4 && x3 - x4
                if len(poin) >= 4:
                    x3 = poin[2][0]
                    y3 = poin[2][1]
                    x4 = poin[3][0]
                    y4 = poin[3][1]

                    if x1 > x4:
                        jarak14 = pc.hitungJarak(x1, x4, y1, y4)
                    elif x4 > x1:
                        jarak14 = pc.hitungJarak(x4, x1, y4, y1)
                    if x2 > x4:
                        jarak24 = pc.hitungJarak(x2, x4, y2, y4)
                    elif x4 > x2:
                        jarak24 = pc.hitungJarak(x4, x2, y4, y2)
                    if x3 > x4:
                        jarak34 = pc.hitungJarak(x3, x4, y3, y4)
                    elif x4 > x3:
                        jarak34 = pc.hitungJarak(x4, x3, y4, y3)

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

            print(jarakMin)

            cv2.waitKey(25)

            self.procWindow.update()


if __name__ == '__main__':
    main_window = tkinter.Tk()

    main_window.title("Deteksi Jarak")
    main_window.geometry("550x250")

    var_rb = IntVar(main_window, 1)
    cam = StringVar()
    coor = []

    pc = Video()

    label1 = tkinter.Label(main_window, text="masukan video untuk deteksi", font="Times 15 bold")
    label1.grid(row=0, column=1)

    # radio btn 1
    rb1 = Radiobutton(main_window, text="Pilih Lokasi Video", variable=var_rb, value=1, command=pc.hide2)
    rb1.grid(row=1, column=0, sticky='W')
    ent1 = tkinter.Entry(main_window)
    ent1.grid(row=2, column=0, sticky='N')
    btn_open = tkinter.Button(main_window, text="Open File", command=pc.btn_openFile)
    btn_open.grid(row=2, column=1, sticky='W')

    # radio btn 2
    rb2 = Radiobutton(main_window, text="Nyalakan Realtime Kamera", variable=var_rb, value=2, command=pc.hide1)
    rb2.grid(row=3, column=0, sticky='W')
    ent2 = tkinter.Entry(main_window, textvariable=cam)
    ent2.grid(row=4, column=0, sticky='N')
    lbl3 = tkinter.Label(main_window, text="Kamera : ")
    lbl3.grid(row=4, column=1, sticky='W')
    lbl2 = tkinter.Label(main_window, text="Camera : ", textvariable=cam)
    lbl2.grid(row=4, column=1, sticky='N')

    # btn mulai
    lbl_empty = tkinter.Label(main_window, text="")
    lbl_empty.grid(row=6, column=1, sticky='N')
    btn_mulai = tkinter.Button(main_window, text="Tinjau Video", command=pc.btn_mulai)
    btn_mulai.grid(row=7, column=1, sticky='N')

    pc.hide2()

    main_window.mainloop()
