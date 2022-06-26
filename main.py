import tkinter
import numpy as np
import cv2
import os
from tkinter import filedialog

main_window = tkinter.Tk()

main_window.title("Deteksi Jarak")
main_window.geometry("500x300")


def btn_openFile():
    main_window.withdraw()

    dir = os.getcwd()
    tempdir = filedialog.askopenfilename(parent=main_window, initialdir=dir, title='Plilih lokasi vidio')

    if len(tempdir) > 0:
        label2 = tkinter.Label(main_window, text=str(tempdir))
        label2.pack()
        print("You chose %s" % tempdir)

    main_window.deiconify()

    cap = cv2.VideoCapture(tempdir)

    # return tempdir


label1 = tkinter.Label(main_window, text="masukan video untuk deteksi")
btn_open = tkinter.Button(main_window, text="Open File", command=btn_openFile)



label1.pack()
btn_open.pack()

main_window.mainloop()
