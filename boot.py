# import the necessary packages
#for run
# python3 boot2.py -o/--ouput
from __future__ import print_function
from PIL import Image
from PIL import ImageTk
import tkinter as tki
import threading
import datetime
import imutils
import cv2
import os


from webcam import *


######conexion con postgres

import psycopg2
from time import time

class PhotoBoothApp:
    def conndb(self, ci, nombre, img_src):
        print("trying to: cosadcasdfasdasd")
        try:
            conn = psycopg2.connect("dbname=reconocimiento user=reddytintayaconde password=123456")  
        except:
            print("error al ingresar algo nuevo dude")
        cur = conn.cursor()
        #sqlquery = "insert into know_users(\""+nombre+"\",\""+img_src+"\") VALUES  (nombre, img_src);"
        sqlquery = "select nombre, img_src from know_users ORDER BY id;"
        cur.execute(sqlquery)
        count = cur.rowcount
        cur.close()
        conn.close()

        conn = psycopg2.connect("dbname=reconocimiento user=reddytintayaconde password=123456")  
        cur = conn.cursor()
        postgres_insert_query = """ INSERT INTO know_users (ci,id, nombre, img_src) VALUES (%s, %s, %s,%s)"""
        record_to_insert = (123,count, nombre, img_src)
        #cur.execute("""INSERT INTO reg (nombre, img_src) VALUES (%s, %s)""", (nombre, img_src))
        cur.execute(postgres_insert_query, record_to_insert)
        conn.commit()
        #ord = 'INSERT INTO know_users (ci, id, nombre, img_src) VALUES (%s, %s, %s, %s)', ('1441', 5 ,nombre, img_src)
        print(ord)
        cur.close()
        conn.close()
    def __init__(self, vs, outputPath):
        self.vs = vs
        self.outputPath = outputPath
        self.frame = None
        self.thread = None
        self.stopEvent = None

        self.root = tki.Tk()
        self.panel = None
        btn = tki.Button(self.root, text="Ok", command=self.takeSnapshot).grid(column=0, row = 3)
        btnContinue = tki.Button(self.root, text="Skip", command= self.skip).grid(column=1, row = 3)
        
        self.txt = tki.Entry(self.root)
        self.txt.grid(column=1, row= 1)
        #self.txt.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)

        lbl = tki.Label(self.root, text= "Ingrese el Nombre").grid(column=0, row= 1)
        #lbl.pack(side="bottom", fill="both", expand="yes", padx=10, pady=10)
        
        self.stopEvent = threading.Event()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()

        self.root.wm_title("Llenar Base de Datos")
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
    def videoLoop(self):
        try:
            while not self.stopEvent.is_set():
                self.frame = self.vs.read()
                self.frame = imutils.resize(self.frame, width=300)
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)
                image = cv2.flip(image, 1)
                image = Image.fromarray(image)
                image = ImageTk.PhotoImage(image)
                
                if self.panel is None:
                    self.panel = tki.Label(image=image)
                    self.panel.image = image
                    self.panel.grid(row = 0, columnspan= 2)
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image
        except RuntimeError:
            print("[INFO] caught a RuntimeError")

    def skip(self):
        rec= Recognition()
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()
        self.onClose()
    def takeSnapshot(self):
        ts = datetime.datetime.now()
        filename = "{}.png".format(self.txt.get())
        print("[info] ", filename)
        p = os.path.sep.join((self.outputPath, filename))
        cv2.imwrite("knowFaces/"+filename, self.frame.copy())
        self.conndb("123", self.txt.get(), filename)

        rec = Recognition()
        self.onClose
    
    def onClose(self):
        self.stopEvent.set()
        self.vs.stop()
        self.root.quit()

