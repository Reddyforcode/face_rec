from tkinter import *
import numpy as np
import cv2
from PIL import Image, ImageTk

video_capture = cv2.VideoCapture(0)

class Test:
    global video_capture
    def __init__(self, parent):
        self.parent = parent
        self.maclasse = MaClasse(self.parent)
        print("repite1")
    def test(self):
        print("repite2")
        self.drawingArea=Canvas(self.parent)

class MaClasse:
    global video_capture
    def __init__(self, parent):
        self.s=600,600,3
        self.ma=np.zeros(self.s,dtype=np.uint8)
        self.top = Toplevel(parent)
        self.top.wm_title("OpenCV Image")
        self.label = Label(self.top)
        self.label.pack()
        while(True):
            self.show_image()
            parent.mainloop()

    def show_image(self):

        print("leyendo..")
        ret, frame = video_capture.read()

        cv2image =cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        self.im = Image.fromarray(cv2image).resize((760, 400))
        self.imgtk = ImageTk.PhotoImage(image=self.im)
        self.label.configure(image=self.imgtk)

if __name__=="__main__":

    root = Tk()
    root.wm_title("Test")
    v = Test(root)
    v.test()
    root.mainloop()
