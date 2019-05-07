import cv2
import face_recognition
from PIL import Image, ImageTk
from videocaptureasync import *

contadorProm = 0
sumaEnc = 0
for i in range (1, 5):
    abel_img =face_recognition.load_image_file("reddy/{}.jpg".format(i))
    encoding =face_recognition.face_encodings(abel_img, num_jitters=100)[0]
    sumaEnc = sumaEnc+encoding
    contadorProm += 1
    print(i)

obama_image = face_recognition.load_image_file("knowFaces/obama.png")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

ted_image = face_recognition.load_image_file("knowFaces/ted.png")
ted_face_encoding = face_recognition.face_encodings(ted_image)[0]

# Load a second sample picture and learn how to recognize it.
reddy_image = face_recognition.load_image_file("knowFaces/reddy.png")
#reddy_face_encoding = face_recognition.face_encodings(reddy_image)[0]
reddy_face_encoding = sumaEnc/contadorProm

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    ted_face_encoding,
    reddy_face_encoding

]
known_face_names = [
    "Barack Obama",
    "Ted",
    "Reddy"
]

cap = VideoCaptureAsync()
#cap.open("rtsp://admin:DocoutBolivia@192.168.1.64:554/Streaming/Channels/102/")
cap.start()

face_locations =[]
face_encodings = []

process_this_frame = True

face_locations
face_encodings
process_this_frame
face_names = []
while (True):
    print("letyendo")
    ret, frame = cap.read()
    small_frame = cv2.resize(frame, (0,0), fx=0.5, fy=0.5)    #1/4 de la resolucion just for testngt
    #small_frame =frame
    rgb_small_frame = small_frame[:, :, ::-1]
    if process_this_frame:
        face_locations = face_recognition.face_locations(small_frame)
        face_encodings =face_recognition.face_encodings(small_frame, face_locations)
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance = 0.40)
            name = "Unknown"
            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]
            face_names.append(name)

    process_this_frame = not process_this_frame
    a = len(face_locations)
    print(a)
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 2
        right *= 2
        bottom *= 2
        left *= 2
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 123), 2)
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)



    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.stop()
cap.release()
cv2.destroyAllWindows()
