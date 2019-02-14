import tkinter as tk
import cv2
from PIL import Image, ImageTk

ventana =tk.Tk()
ventana.geometry("300x744+0+0")
ventana.config(bg = "white")
ventana.title("Usuarios Identifiados")
#configuracion para el grid
ventana.columnconfigure(0, weight = 1)
ventana.columnconfigure(1, weight = 1)
ventana.rowconfigure(0, weight =1)
ventana.rowconfigure(1, weight =1)
ventana.rowconfigure(2, weight =1)
ventana.rowconfigure(3, weight =1)
ventana.rowconfigure(4, weight =1)
#variabeles globales donde se almacenan las imagenes
paths = ["face-10.png", "face-11.png", "face-12.png", "face-13.png", "face-14.png", "face-15.png", "face-16.png", "face-17.png"]

#calcualr la escala para darle zoom a las imagenes y se acomoden con el resto
def rescale(photoImg):
    scale_w = int(ventana.winfo_reqwidth()/int(photoImg.width()))
    scale_h = int(ventana.winfo_reqheight()/int(photoImg.height()))
    photoImg = photoImg.zoom(scale_w, scale_h)
    return photoImg

#path img tomada imagen base de datos
def newImages(imgTomada, imgDB):
    image_4_2 = image_3_2
    image_4_1 = image_3_1
    image_3_2 = image_2_2
    image_3_1 = image_2_1
    image_2_2 = image_1_2
    image_2_1 = image_1_1
    image_1_1 = tk.PhotoImage(file = imgTomada)
    image_1_2 = tk.PhotoImage(file = imgDB)
##pasar imagenes con formato png

#string con el path de las imagenes a mostrar
#solo se va a lanzar al inicio para llenar la parte del registro
def cargarPathImg(paths):
    #tamaño de array: 8

    images = []
    images.clear()
    image_1_1 = rescale(tk.PhotoImage(file = paths[0]))
    images.append(image_1_1)
    image_1_2 = rescale(tk.PhotoImage(file = paths[1]))
    images.append(image_1_2)

    image_2_1 = rescale(tk.PhotoImage(file = paths[2]))
    images.append(image_2_1)
    image_2_2 = rescale(tk.PhotoImage(file = paths[3]))
    images.append(image_2_2)

    image_3_1 = rescale(tk.PhotoImage(file = paths[4]))
    images.append(image_3_1)
    image_3_2 = rescale(tk.PhotoImage(file = paths[5]))
    images.append(image_3_2)

    image_4_1 = rescale(tk.PhotoImage(file = paths[6]))
    images.append(image_4_1)
    image_4_2 = rescale(tk.PhotoImage(file = paths[7]))
    images.append(image_4_2)
    return images

def colocarImagenesGrid(images):

    """
    lblImage_1_1 = tk.Label(ventana, image =image_1_1).grid(column = 0, row =0, sticky = 'NSEW')
    lblImage_1_2 = tk.Label(ventana, image =image_1_2).grid(column = 1, row =0, sticky = 'NSEW')

    lblImage_2_1 = tk.Label(ventana, image =image_2_1).grid(column = 0, row =1, sticky = 'NSEW')
    lblImage_2_2 = tk.Label(ventana, image =image_2_2).grid(column = 1, row =1, sticky = 'NSEW')

    lblImage_3_1 = tk.Label(ventana, image =image_3_1).grid(column = 0, row =2, sticky = 'NSEW')
    lblImage_3_2 = tk.Label(ventana, image =image_3_2).grid(column = 1, row =2, sticky = 'NSEW')

    lblImage_4_1 = tk.Label(ventana, image =image_4_1).grid(column = 0, row =3, sticky = 'NSEW')
    lblImage_4_2 = tk.Label(ventana, image =image_4_2).grid(column = 1, row =3, sticky = 'NSEW')
    """

    lblImage_1_1 = tk.Label(ventana, image =images[0]).grid(column = 0, row =1, sticky = 'NSEW')
    lblImage_1_2 = tk.Label(ventana, image =images[1]).grid(column = 1, row =1, sticky = 'NSEW')

    lblImage_2_1 = tk.Label(ventana, image =images[2]).grid(column = 0, row =2, sticky = 'NSEW')
    lblImage_2_2 = tk.Label(ventana, image =images[3]).grid(column = 1, row =2, sticky = 'NSEW')

    lblImage_3_1 = tk.Label(ventana, image =images[4]).grid(column = 0, row =3, sticky = 'NSEW')
    lblImage_3_2 = tk.Label(ventana, image =images[5]).grid(column = 1, row =3, sticky = 'NSEW')

    lblImage_4_1 = tk.Label(ventana, image =images[6]).grid(column = 0, row =4, sticky = 'NSEW')
    lblImage_4_2 = tk.Label(ventana, image =images[7]).grid(column = 1, row =4, sticky = 'NSEW')

def clicked():
    imageR = imageL
    print("pressed")
    print(ventana.winfo_reqwidth(), " , ", ventana.winfo_reqheight())
images = cargarPathImg(paths)
print(len(images))
colocarImagenesGrid(images)



ventana.mainloop()
