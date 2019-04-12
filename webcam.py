import face_recognition
import cv2
import psycopg2
from PIL import Image
from time import time
from videocaptureasync import VideoCaptureAsync
import numpy as np 
from time import gmtime, strftime

class Persona:
    def __init__(self, img_source, nombre):
        self.img_source =img_source
        self.nombre = nombre
    def getNombre(self):
        return self.nombre
    def getImgSrc(self):
        return self.img_source

def getKnowPersonsFromDB():
    know_persons = []
    try:
        conn = psycopg2.connect("dbname=registros user=reddy password=123456 port=5432 host=localhost port=5432")
        
    except:
        print("fallo conn")
    cur =conn.cursor()
    sqlquery = "select nombre, img_src from know_users ORDER BY id;"
    cur.execute(sqlquery)
    row =cur.fetchone()
    while row is not None:
        print(row)
        know_persons.append(Persona("knowFaces/"+row[1], row[0]))
        print(know_persons[len(know_persons)-1].getNombre())    #print names
        row = cur.fetchone()
    cur.close()
    conn.close()
    return know_persons

class Recognition():

    #parametros globales para la segunda ventana
    def distance(self, accuracy):
        #pasar dos encodings procesa el nivel de accuracy de cada uno y devuelve un loading bar
        load = accuracy * 270
        color = (0, 0, 255)
        image = np.zeros((30, 300, 3), np.uint8)
        cv2.rectangle(image, (0, 0), (300, 50), (81, 88, 94), cv2.FILLED)
        cv2.rectangle(image, (10, 15), (int(load)+15, 20), color, cv2.FILLED)
        return image
    def record_date_hour(self, name):
        #insert where name date
        date = strftime("%Y/%m/%d", gmtime())
        hour = strftime("%H:%M:%S", gmtime())

    def dahua(self, name, actual_img, accuracy):
        path = "knowFaces/" + name.lower() + ".png"
        db_img = cv2.imread(path)
        db_img = cv2.resize(db_img, (150, 150), interpolation=cv2.INTER_CUBIC)
        un_img = np.concatenate((db_img, actual_img), axis = 1)
        un_img = np.concatenate((un_img, self.distance(accuracy)), axis = 0)
        if(self.first):
            self.first = False
            cv2.imshow("Board", un_img)
        else:
            final = np.concatenate((un_img, self.pastUnion), axis = 0)
            cv2.imshow("Board", final)
        self.pastUnion = un_img
        return

    def getEncodingFaces(self, know_persons):
        i = 1
        for imag in know_persons:
            image = face_recognition.load_image_file(imag.getImgSrc())
            self.faces_encoding.append(face_recognition.face_encodings(image)[0])
            self.face_names.append(imag.getNombre())
            i = i + 1
        return self.faces_encoding, self.face_names

    def __init__(self):
        self.pastUnion = 2
        self.first = True
        self.path = "knowFaces/reddy.png"
        self.db_img = cv2.imread(self.path)
        self.db_img = cv2.resize(self.db_img, (150, 150), interpolation=cv2.INTER_CUBIC)
        self.cap = VideoCaptureAsync()
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
        self.cap.start()
        self.face_record1 = "nadies"
        self.nombres = {}
        self.first = True
        self.accuracy = 2

        self.know_persons = getKnowPersonsFromDB()
        self.faces_encoding = []
        self.face_names = []
        self.known_face_encodings, self.known_face_names = self.getEncodingFaces(self.know_persons)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True

        while True:
            ret, frame = self.cap.read()
            small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)    #mitad de la calidad
            rgb_small_frame = small_frame[:, :, ::-1]
            if self.process_this_frame:
                self.face_locations = face_recognition.face_locations(rgb_small_frame)#, model ="cnn")
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                self.face_names = []
                self.face_values = []

                for face_encoding in self.face_encodings:
                    self.matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    self.name = "Unknown"
                    self.values = np.linalg.norm(self.known_face_encodings-face_encoding, axis = 1)

                    if True in self.matches:
                        first_match_index = self.matches.index(True)
                        self.accuracy = self.values[first_match_index]    #get the accuracy
                        self.name = self.known_face_names[first_match_index]
                    self.face_names.append(self.name)
                    self.face_values.append(self.accuracy)    #gui
                    
            self.process_this_frame = not self.process_this_frame

            tratar =False
            for (top, right, bottom, left), name, acc in zip(self.face_locations, self.face_names, self.face_values):
                top *= 4
                right *= 4
                bottom *= 4
                left *= 4
                
                actual_img = cv2.resize(frame[top:bottom, left:right], (150, 150), interpolation=cv2.INTER_CUBIC)    #gui
                cv2.rectangle(frame, (left, top), (right, bottom), (123, 123, 123), 2)  #face bordes
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (123, 123, 123), cv2.FILLED) #space for name
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 0), 1)
                print("nombres: ", self.nombres)

                try:
                    if(self.nombres[self.name]>=1):
                        self.nombres[self.name] +=1
                    else:
                        self.nombres[self.name] = 1

                except:
                    print("entrando excepcion")
                    self.nombres[self.name] = 1

                if(name!="Unknown" and self.nombres[self.name] == 7):
                    if(self.face_record1 != self.name):
                        self.dahua(self.name, actual_img, acc)#causa 50fps con 0.02 y el mas bajo 0.001
                        self.face_record1 = name
                    self.nombres[self.name] = 1
                
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.stop()
        cv2.destroyAllWindows()

rec = Recognition()