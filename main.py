from doctest import master
from tkinter import messagebox
import tkinter
import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import *

from PIL import ImageTk, Image


class Video:

    def __init__(self):
        self.curdir = ""
        self.tempdir = ""
        self.cap = ""

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
                pc.openPrevWindow(self.cap)

        elif var_rb.get() == 2:
            path = ent2.get()
            if path == "":
                pc.msgBox2()
            else:
                main_window.withdraw()
                self.cap = cv2.VideoCapture(int(path))
                pc.openPrevWindow(self.cap)

    def clearValue(self):
        del coor[:]

    def msgBox1(self):
        messagebox.showerror("Kesalahan", "Jumlah koordinat tidak boleh lebih dari 4!")

    def msgBox2(self):
        messagebox.showerror("Kesalahan", "Video yang akan ditinjau tidak boleh kosong!")

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

    def openPrevWindow(self, cap):
        newWindow = Toplevel(master)

        newWindow.title("New Window")
        newWindow.grid_rowconfigure(0, weight=1)
        newWindow.grid_columnconfigure(0, weight=1)

        frame1 = Frame(newWindow)
        frame1.grid(row=0, column=0)

        lbltext1 = Label(frame1, text="Tentukan wilayah deteksi", font="Times 22 bold")
        lbltext1.grid(row=1)

        lblvideo = Label(frame1)
        lblvideo.grid(row=2)

        btnBack = Button(frame1, text="Kembali", command=lambda:[main_window.deiconify(), newWindow.destroy()], width=20, font="bold")
        btnBack.grid(row=3, column=0, sticky=W, pady=15)

        btnClear = Button(frame1, text="Hapus", command=pc.clearValue, width=20, font="bold")
        btnClear.grid(row=3, column=0, pady=15)

        btnProses = Button(frame1, text="Proses", command=pc.clearValue, width=20, font="bold")
        btnProses.grid(row=3, column=0, sticky=E, pady=15)

        newWindow.protocol("WM_DELETE_WINDOW", pc.disable_event)

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
            newWindow.update()

if __name__ == '__main__':
    main_window = tkinter.Tk()

    main_window.title("Deteksi Jarak")
    main_window.geometry("500x250")

    var_rb = IntVar(main_window, 1)
    cam = StringVar()
    coor = []

    pc = Video()

    label1 = tkinter.Label(main_window, text="masukan video untuk deteksi")
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
