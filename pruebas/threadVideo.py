#ya funciona

from threading import Thread, Lock
import cv2
import numpy as np
class WebcamVideoStream :
    def __init__(self, src = 0, width = 320, height = 240) :
        self.stream = cv2.VideoCapture(src)
        self.stream.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, width)
        self.stream.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, height)
        (self.grabbed, self.frame) = self.stream.read()
        self.started = False
        self.read_lock = Lock()

    def start(self) :
        if self.started :
            print ("already started!!")
            return None
        self.started = True
        self.thread = Thread(target=self.update, args=())
        self.thread.start()
        return self

    def update(self) :
        while self.started :
            (grabbed, frame) = self.stream.read()
            self.read_lock.acquire()
            self.grabbed, self.frame = grabbed, frame
            self.read_lock.release()

    def read(self) :
        self.read_lock.acquire()
        frame = self.frame.copy()
        self.read_lock.release()
        return frame

    def stop(self) :
        self.started = False
        if self.thread.is_alive():
            self.thread.join()

    def __exit__(self, exc_type, exc_value, traceback) :
        self.stream.release()

if __name__ == "__main__" :
    vs = cv2.VideoCapture()
    vs.open("rtsp://admin:DocoutBolivia@192.168.1.64:554/Streaming/Channels/102/")

    #vs = WebcamVideoStream().start()
    while True :
        
        cap, frame = vs.read()
        #frame = np.array(frame)
        cv2.imshow('webcam', frame)
        if cv2.waitKey(1) == 27 :
            break

cap.release()
cv2.destroyAllWindows()