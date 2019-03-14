import face_recognition
import cv2
import psycopg2
from PIL import Image
from time import time

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
        conn = psycopg2.connect("dbname=reconocimiento user=reddytintayaconde password=123456")
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
    except:
        print("DB error")
    print(know_persons)

class Recognition():

    def getEncodingFaces(self, know_persons):

        print("length   ",len(know_persons))
        
        print("el tamaño de know persons es : ", len(know_persons))
        i = 1
        for imag in know_persons:
            #if(len(know_persons) > 3 ):
            #    break
            print("para " , " la imagen es: ", imag.getImgSrc())
            image = face_recognition.load_image_file(imag.getImgSrc())
            self.faces_encoding.append(face_recognition.face_encodings(image)[0])
            self.face_names.append(imag.getNombre())
            print("obteniendo...", imag.getNombre())
            i = i + 1
        return self.faces_encoding, self.face_names

    def __init__(self):

        self.video_capture = cv2.VideoCapture(0)
        print("leyendo base de datos")
        self.know_persons = getKnowPersonsFromDB()
        self.faces_encoding = []
        self.face_names = []
        self.known_face_encodings, self.known_face_names = self.getEncodingFaces(self.know_persons)
        self.face_locations = []
        self.face_encodings = []
        self.face_names = []
        self.process_this_frame = True
        i = 0
        while True:
            start_time = time()
            print(i)
            i = i+1
            ret, frame = self.video_capture.read()
            #small_frame = cv2.resize(frame, (0, 0), fx=0.10, fy=0.10)
            small_frame = cv2.resize(frame, (0, 0), fx=0.5, fy=0.5)    #mitad de la calidad
            rgb_small_frame = small_frame[:, :, ::-1]
            if self.process_this_frame:
                self.face_locations = face_recognition.face_locations(rgb_small_frame)#, model ="cnn")
                self.face_encodings = face_recognition.face_encodings(rgb_small_frame, self.face_locations)
                self.face_names = []
                for face_encoding in self.face_encodings:
                    self.matches = face_recognition.compare_faces(self.known_face_encodings, face_encoding)
                    self.name = "Unknown"
                    if True in self.matches:
                        first_match_index = self.matches.index(True)
                        self.name = self.known_face_names[first_match_index]
                    self.face_names.append(self.name)
                    
            self.process_this_frame = not self.process_this_frame


            tratar =False
            for (top, right, bottom, left), name in zip(self.face_locations, self.face_names):
                """top *= 10
                right *= 10
                bottom *= 10
                left *= 10
                """
                #mitad de la calidad
                top *= 2
                right *= 2
                bottom *= 2
                left *= 2
                
                cv2.rectangle(frame, (left, top), (right, bottom), (123, 123, 123), 2)  #face bordes
                cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (123, 123, 123), cv2.FILLED) #space for name
                cv2.putText(frame, name, (left + 6, bottom - 6), cv2.FONT_HERSHEY_DUPLEX, 1.0, (255, 255, 0), 1)
                """
                #agregado fallido **GPU**
                if(name == "Unknown"):
                    face_image =frame[top:bottom, left:right]
                    pil_image = Image.fromarray(face_image)
                    pil_image.save("face-{}.png".format(i))
                    know_persons.append(Persona("face-{}.png".format(i), "face-{}".format(i)))
                    i = i + 1
                    tratar = True
            if (tratar):
                known_face_encodings, known_face_names = getEncodingFaces(know_persons)
                tratar = False
                """
            cv2.imshow('Video', frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elapsed_time =time() - start_time
            print("tiempo: ", elapsed_time)

        self.video_capture.release()
        cv2.destroyAllWindows()