from tkinter import *
from PIL import Image
from PIL import ImageTk
#import tkFileDialog
from tkinter import filedialog
import cv2
from webcam import *

def select_image():
	# grab a reference to the image panels
	global panelA, panelB
	path = filedialog.askopenfilename()




from tkinter import *
nombre = ""
pass_to_cv = False
class Main_screen(Frame):
    def __init__(self,master):
        Frame.__init__(self, master)
        self.grid()
        self.text = Label(text="first")
        self.text.grid()
        root.withdraw()
        print(nombre, " este es")
        self.create_login()

    def create_login(self):
        self.root2 = Toplevel()
        self.app2 = Login_screen(self.root2)


class Login_screen(Frame):
    def __init__(self,master):
        Frame.__init__(self,master)
        self.grid()
        self.lblName = Label(self, text="Name").grid(row=0)
        self.name = Entry(self)
        self.name.grid(row = 1)
        self.botao1 = Button(self, text="Appear",command = lambda: self.show_entry_fields())
        self.botao1.grid()

    def show_entry_fields(self):
        print("First Name: %s" % (self.name.get()))
        nombre = self.name.get()
        pass_to_cv = True
        self.master.destroy()
        
        rec = Recognition()
        root.deiconify()
    def show_main(self):
        self.master.destroy()
        root.deiconify()

root = Tk()
app = Main_screen(root)
root.mainloop()