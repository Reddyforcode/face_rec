import face_recognition
import cv2

# input de la camarad
video_capture = cv2.VideoCapture(0)

# Load a sample picture and learn how to recognize it.
obama_image = face_recognition.load_image_file("obama.jpg")
obama_face_encoding = face_recognition.face_encodings(obama_image)[0]

ted_image = face_recognition.load_image_file("ted.jpg")
ted_face_encoding = face_recognition.face_encodings(ted_image)[0]

# Load a second sample picture and learn how to recognize it.
biden_image = face_recognition.load_image_file("reddy.jpg")
biden_face_encoding = face_recognition.face_encodings(biden_image)[0]

# Create arrays of known face encodings and their names
known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding,
    ted_face_encoding
]
known_face_names = [
    "Barack Obama",
    "Reddy",
    "Ted"
]

# Initialize some variables
face_locations = []
face_encodings = []
face_names = []
process_this_frame = True
antNumberFaces = 0
face_numbers = 0

#cantidad de rostros en una imagen
def numberFaces(face_locations):
    return len(face_locations)
    
while True:
    ret, frame = video_capture.read()

    # un cuarto del tamaño original de la camara
    small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

    rgb_small_frame = small_frame[:, :, ::-1] #bgr(opencv) a rgb(face_reognition)

    # Only process every other frame of video to save time
    if process_this_frame:
        # Find all the faces and face encodings in the current frame of video
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)
        
        #face_number guarda la cantidad de rostros
        face_numbers = numberFaces(face_locations)
        

        face_names = []
        #match 
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            # If a match was found in known_face_encodings, just use the first one.
            if True in matches:
                first_match_index = matches.index(True)
                name = known_face_names[first_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    # Display the results
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        # Scale back up face locations since the frame we detected in was scaled to 1/4 size
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        # Draw a box around the face
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        # Draw a label with a name below the face
        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)


    #if (face_numbers != antNumberFaces):
    font = cv2.FONT_HERSHEY_DUPLEX
    cv2.putText(frame, str(face_numbers), (20, 40), font, 1.0, (255, 0, 255), 1)
    antNumberFaces = face_numbers
    cv2.imshow('Video', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()