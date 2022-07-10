from tkinter import messagebox

import cv2
import numpy as np
import tkinter
from tkinter import *
from PIL import ImageTk, Image

def clearValue():
    del coor[:]

def msgBox():
    messagebox.showerror("Kesalahan", "Jumlah koordinat tidak boleh lebih dari 4!")


def displayCoordinates(event):
    if(len(coor)<4):
        coor.append([event.x, event.y])
        print(coor)
        print(len(coor))
    else:
        msgBox()


def video_stream():
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
        lblvideo.bind('<Button-1>', displayCoordinates)

        cv2.waitKey(25)
        window.update()


cap = cv2.VideoCapture("video/pedestrian2.mp4")

coor = []

window = Tk()
window.title("Main window")
window.grid_rowconfigure(0, weight=1)
window.grid_columnconfigure(0, weight=1)

frame1 = Frame(window)
frame1.grid(row=0, column=0)

lbltext1 = Label(frame1, text="Tentukan wilayah deteksi", font="Times 22 bold")
lbltext1.grid(row=1)

lblvideo = Label(frame1)
lblvideo.grid(row=2)

btnClear = Button(frame1, text="Hapus", command=clearValue, width=30, font="bold")
btnClear.grid(row=3, column=0, sticky=W, pady=15)

btnProses = Button(frame1, text="Proses", command=clearValue, width=30, font="bold")
btnProses.grid(row=3, column=0, sticky=E, pady=15)

video_stream()
window.mainloop()
cap.release()
cv2.destroyAllWindows()
