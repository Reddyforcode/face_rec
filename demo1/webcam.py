import face_recognition
import cv2
import psycopg2
from PIL import Image
from time import time
from videocaptureasync import VideoCaptureAsync
import numpy as np 
from time import gmtime, strftime
import dlib
import face_recognition_models


face_recognition_model = face_recognition_models.face_recognition_model_location()
face_encoder = dlib.face_recognition_model_v1(face_recognition_model)

predictor_68_point_model = face_recognition_models.pose_predictor_model_location()
pose_predictor_68_point = dlib.shape_predictor(predictor_68_point_model)

cnn_face_detection_model = face_recognition_models.cnn_face_detector_model_location()
cnn_face_detector = dlib.cnn_face_detection_model_v1(cnn_face_detection_model)


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
        start=time()
        print(row)
        know_persons.append(Persona("knowFaces/"+row[1], row[0]))
        print(know_persons[len(know_persons)-1].getNombre())    #print names
        row = cur.fetchone()
        print("consulta: ", time()-start)
    cur.close()
    conn.close()
    return know_persons

class Recognition():

    #parametros globales para la segunda ventana
    def distance(self, accuracy, name):
        #pasar dos encodings procesa el nivel de accuracy de cada uno y devuelve un loading bar
        load = accuracy * 270
        color = (0, 0, 255)
        image = np.zeros((40, 300, 3), np.uint8)
        cv2.rectangle(image, (0, 0), (300, 50), (255, 255, 255), cv2.FILLED)
        cv2.putText(image, name, (10, 15), cv2.FONT_HERSHEY_DUPLEX, 0.5, (125, 125, 0), 1)
        cv2.rectangle(image, (10, 20), (int(load)+15, 30), color, cv2.FILLED)
        return image
    
    def _css_to_rect(self, css):
        """
        Convert a tuple in (top, right, bottom, left) order to a dlib `rect` object
        :param css:  plain tuple representation of the rect in (top, right, bottom, left) order
        :return: a dlib `rect` object
        """
        return dlib.rectangle(css[3], css[0], css[1], css[2])
    
    def _raw_face_landmarks(self, face_image, face_locations=None, model="large"):
        face_locations = None   
        if face_locations is None:
            face_locations = cnn_face_detector(face_image, 1)
            face_locations = [self._css_to_rect(face_location) for face_location in face_locations]
        else:
            face_locations = [self._css_to_rect(face_location) for face_location in face_locations]

        pose_predictor = pose_predictor_68_point

        return [pose_predictor(face_image, face_location) for face_location in face_locations]

    def record_date_hour(self, name):
        #insert where name date
        date = strftime("%Y/%m/%d", gmtime())
        hour = strftime("%H:%M:%S", gmtime())
        try:
            connection = psycopg2.connect("dbname=registros user=reddy password=123456 port=5432 host=localhost port=5432")
        except:
            print("conexion exito")
        cursor = connection.cursor()
        postgres_insert_query = """ INSERT INTO deteccion (name, fecha, hora) VALUES (%s, %s, %s)"""
        
        fecha = "'"+date+"'"
        hora = "'"+ hour +"'"
        record_to_insert = (name, fecha, hora)
        cursor.execute(postgres_insert_query, record_to_insert)
        connection.commit()
        cursor.close()
        connection.close()


    def dahua(self, name, actual_img, accuracy):
        path = "knowFaces/" + name.lower() + ".png"
        db_img = cv2.imread(path)
        db_img = cv2.resize(db_img, (150, 150), interpolation=cv2.INTER_CUBIC)
        un_img = np.concatenate((db_img, actual_img), axis = 1)
        un_img = np.concatenate((un_img, self.distance(accuracy, name)), axis = 0)
        self.record_date_hour(name)
        if(self.first):
            self.first = False
            cv2.imshow("Board", un_img)
        else:
            final = np.concatenate((un_img, self.pastUnion), axis = 0)
            cv2.imshow("Board", final)
        self.pastUnion = un_img

        return
    def face_enc(self, face_image, known_face_locations=None, num_jitters=1):
    
        raw_landmarks = face_recognition.api._raw_face_landmarks(face_image, known_face_locations)
        return [np.array(face_encoder.compute_face_descriptor(face_image, raw_landmark_set, num_jitters)) for raw_landmark_set in raw_landmarks]


    def getEncodingFaces(self, know_persons):
        i = 1
        for imag in know_persons:
            image = face_recognition.load_image_file(imag.getImgSrc())
            #self.faces_encoding.append(face_recognition.face_encodings(image, num_jitters=100)[0])

            self.face_names.append(imag.getNombre())
            if(imag.getNombre() == "reddy"):
                enc1= self.face_enc(image, num_jitters=100)[0]

                img2 = face_recognition.load_image_file("knowFaces/reddy2.png")
                enc2= self.face_enc(img2, num_jitters=100)[0]

                img3 = face_recognition.load_image_file("knowFaces/reddy1.png")
                enc3= self.face_enc(img3, num_jitters=100)[0]

                promedio = (enc1+enc2+enc3)/3


                self.faces_encoding.append(promedio)
            else:
                self.faces_encoding.append(self.face_enc(image, num_jitters=100)[0])



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
        
        frame_width = 1280
        frame_height = 720

        # Define the codec and create VideoWriter object.The output is stored in 'outpy.avi' file.

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
            small_frame = cv2.resize(frame, (0, 0), fx=1, fy=1)
            #mitad de la calidad
            rgb_small_frame = small_frame[:, :, ::-1]
            if self.process_this_frame:
                self.face_locations = face_recognition.face_locations(rgb_small_frame, model="cnn")#, model ="cnn")
                self.face_encodings = self.face_enc(rgb_small_frame, self.face_locations,  num_jitters=100)
                self.face_names = []
                self.face_values = []

                for face_encoding in self.face_encodings:
                    self.matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding, tolerance= 0.30)
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
                """top *= 2
                right *= 2
                bottom *= 2
                left *= 2"""
                collight = (115, 115, 115)
                actual_img = cv2.resize(frame[top:bottom, left:right], (150, 150), interpolation=cv2.INTER_CUBIC)    #gui
                cv2.rectangle(frame, (left, top), (right, bottom), collight, 1)  #face bordes
                ##calcular el tamaño entre top y left 
                vertical = bottom-top
                horizontal = right - left
                #draw contorns
                r = right
                l = left

                t = top
                b = bottom
                
                alpha = vertical / 4
                alpha = int(alpha)
                betha = 2 * alpha
                if(name == "Unknown"):
                    col = (255, 255, 255)

                else:
                    col = (241, 175, 14)
                cv2.line(frame, (l, t), (l, t+alpha), col, 2)
                cv2.line(frame, (l, t), (l+alpha, t), col, 2)

                cv2.line(frame, (r, t), (r-alpha, t), col, 2)
                cv2.line(frame, (r, t), (r, t+alpha), col, 2)

                cv2.line(frame, (l, b), (l+alpha, b), col, 2)
                cv2.line(frame, (l, b), (l, b-alpha), col, 2)

                cv2.line(frame, (r, b), (r-alpha, b), col, 2)
                cv2.line(frame, (r, b), (r, b-alpha), col, 2)
                
                alpha = 10
                cv2.line(frame, (l-alpha, t+betha), (l+alpha, t+betha), collight, 2)
                cv2.line(frame, (r-alpha, t+betha), (r+alpha, t+betha), collight, 2)
                cv2.line(frame, (l+betha, t-alpha), (l+betha, t+alpha), collight, 2)
                cv2.line(frame, (l+betha, b-alpha), (l+betha, b +alpha), collight, 2)
                
                #print("vertical: ", vertical)
                #print("horizontal: ", horizontal)

                #cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (123, 123, 123), cv2.FILLED) #space for name
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 0.70, (255, 255, 0), 1)
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
            #self.out.write(frame)
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

       
        self.cap.stop()
        #print(self.out.release())
        ##out.release()
        cv2.destroyAllWindows()

rec = Recognition()