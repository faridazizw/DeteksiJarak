import yoloObjectDetection
import tkinter
import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import *


class Video:

    def __init__(self):
        self.curdir = ""
        self.tempdir = ""

    def btn_openFile(self):
        main_window.withdraw()

        self.curdir = os.getcwd()
        self.tempdir = filedialog.askopenfilename(parent=main_window, initialdir=self.curdir,
                                                  title='Plilih lokasi vidio', filetypes=[
                ("all video format", ".mp4"),
                ("all video format", ".flv"),
                ("all video format", ".avi"),
            ])

        ent1.insert(0, str(self.tempdir))

        main_window.deiconify()
        return self.tempdir

    def btn_mulai(self):
        if var.get() == 1:
            path = ent1.get()
            cap = cv2.VideoCapture(path)

            if (cap.isOpened() == False):
                print("Error opening video  file")

            while (cap.isOpened()):

                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:

                    # Display the resulting frame
                    cv2.imshow('Frame', frame)

                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

                # Break the loop
                else:
                    break

        elif var.get() == 2:
            path = ent2.get()
            cap = cv2.VideoCapture(int(path))

            if (cap.isOpened() == False):
                print("Error opening video  file")

            while (cap.isOpened()):

                # Capture frame-by-frame
                ret, frame = cap.read()
                if ret == True:

                    # Display the resulting frame
                    cv2.imshow('Frame', frame)

                    # Press Q on keyboard to  exit
                    if cv2.waitKey(25) & 0xFF == ord('q'):
                        break

                # Break the loop
                else:
                    break

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


if __name__ == '__main__':
    main_window = tkinter.Tk()

    main_window.title("Deteksi Jarak")
    main_window.geometry("500x250")

    var = IntVar(main_window, 1)
    cam = StringVar()

    pc = Video()

    label1 = tkinter.Label(main_window, text="masukan video untuk deteksi")
    label1.grid(row=0, column=1)

    # radio btn 1
    rb1 = Radiobutton(main_window, text="Pilih Lokasi Video", variable=var, value=1, command=pc.hide2)
    rb1.grid(row=1, column=0, sticky='W')
    ent1 = tkinter.Entry(main_window)
    ent1.grid(row=2, column=0, sticky='N')
    btn_open = tkinter.Button(main_window, text="Open File", command=pc.btn_openFile)
    btn_open.grid(row=2, column=1, sticky='W')

    # radio btn 2
    rb2 = Radiobutton(main_window, text="Nyalakan Realtime Kamera", variable=var, value=2, command=pc.hide1)
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
    btn_mulai = tkinter.Button(main_window, text="Mulai Video", command=pc.btn_mulai)
    btn_mulai.grid(row=7, column=1, sticky='N')

    pc.hide2()

    main_window.mainloop()
