import cv2
import face_recognition
import tkinter as tk
from tkinter import *
import ttk
from ttk import Frame
from PIL import Image, ImageTk

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

white 		= "#ffffff"
lightBlue2 	= "#adc5ed"
font 		= "Constantia"
fontButtons = (font, 12)
maxWidth  	= 800
maxHeight 	= 480

#Graphics window
mainWindow = tk.Tk()
mainWindow.configure(bg=lightBlue2)
mainWindow.geometry('%dx%d+%d+%d' % (maxWidth,maxHeight,0,0))
mainWindow.resizable(0,0)
# mainWindow.overrideredirect(1)

mainFrame = Frame(mainWindow)
mainFrame.place(x=20, y=20)

#Capture video frames
lmain = tk.Label(mainFrame)
lmain.grid(row=0, column=0)

cap = cv2.VideoCapture(0)

face_locations =[]
face_encodings = []

process_this_frame = True
def show_frame():
	global face_locations
	global face_encodings
	global process_this_frame
	face_names = []

	print("letyendo")
	ret, frame = cap.read()
	small_frame = cv2.resize(frame, (0,0), fx=0.25, fy=0.25)    #1/4 de la resolucion just for testngt
	#small_frame =frame
	rgb_small_frame = small_frame[:, :, ::-1]
	if process_this_frame:
		face_locations = face_recognition.face_locations(small_frame)
		face_encodings =face_recognition.face_encodings(small_frame, face_locations)
		for face_encoding in face_encodings:
			matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
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
		top *= 4
		right *= 4
		bottom *= 4
		left *= 4
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 123), 2)
		cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

	cv2image  = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

	img   = Image.fromarray(cv2image).resize((760, 400))
	imgtk = ImageTk.PhotoImage(image = img)

	lmain.imgtk = imgtk
	lmain.configure(image=imgtk)
	lmain.after(1,show_frame)

show_frame()  #Display
mainWindow.mainloop()  #Starts GUI
