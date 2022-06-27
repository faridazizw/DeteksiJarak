import tkinter
import numpy as np
import cv2
import os
from tkinter import filedialog
from tkinter import *

main_window = tkinter.Tk()

main_window.title("Deteksi Jarak")
main_window.geometry("500x250")


def btn_openFile():
    main_window.withdraw()

    curdir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent=main_window, initialdir=curdir, title='Plilih lokasi vidio')

    ent1.insert(0, str(tempdir))

    main_window.deiconify()
    return tempdir


def hide1():
    ent1.config(state='disabled')
    ent2.config(state='normal')
    lbl2.config(state='active')
    btn_open.config(state='disabled')


def hide2():
    ent1.config(state='normal')
    ent2.config(state='disabled')
    lbl2.config(state='disabled')
    btn_open.config(state='active')


var = IntVar(main_window, 1)
cam = StringVar()

label1 = tkinter.Label(main_window, text="masukan video untuk deteksi")
label1.grid(row=0, column=1)

# radio btn 1
rb1 = Radiobutton(main_window, text="Pilih Lokasi Video", variable=var, value=1, command=hide2)
rb1.grid(row=1, column=0, sticky='W')
ent1 = tkinter.Entry(main_window)
ent1.grid(row=2, column=0)
btn_open = tkinter.Button(main_window, text="Open File", command=btn_openFile)
btn_open.grid(row=2, column=1, sticky='W')

# radio btn 2
rb2 = Radiobutton(main_window, text="Nyalakan Realtime Kamera", variable=var, value=2, command=hide1)
rb2.grid(row=3, column=0, sticky='W')
ent2 = tkinter.Entry(main_window, textvariable=cam)
ent2.grid(row=4, column=0)
lbl3 = tkinter.Label(main_window, text="Kamera : ")
lbl3.grid(row=4, column=1, sticky='W')
lbl2 = tkinter.Label(main_window, text="Camera : ", textvariable=cam)
lbl2.grid(row=4, column=1, sticky='N')


hide2()

main_window.mainloop()
