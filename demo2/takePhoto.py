import cv2

cap = cv2.VideoCapture("rtsp://admin:DocoutBolivia@192.168.1.64:554/Streaming/Channels/102/")

while(True):
    _, frame = cap.read()
    cv2.imshow("frame", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("BREAK;")
        cv2.imwrite("phot.jpg", frame)
        break
cv2.waitKey(0)
cv2.destroyAllWindows()