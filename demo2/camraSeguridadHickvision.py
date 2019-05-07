import numpy as np
import cv2
from hikvisionapi import Client


cap = cv2.VideoCapture()
#cap.open("rtsp://admin:DocoutBolivia@192.168.1.64:554/h264/ch0/sub")
cap.open("rtsp://admin:DocoutBolivia@192.168.1.64:554/Streaming/Channels/102/")
#cam = Client('http://192.168.1.64', 'admin', 'DocoutBolivia')

#rtsp://admin:password@192.168.1.64/h264/ch1/sub/

#response = cam.System.deviceInfo(method='get')
ret, frame = cap.read()
cv2.imwrite("holo.jpg", frame)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here

    # Display the resulting frame
    cv2.imshow('frame',frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break