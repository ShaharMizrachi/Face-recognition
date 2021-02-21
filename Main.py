from API import *
import cv2


vid = cv2.VideoCapture(0)
faces = []
encodings = []
count = 0
getAllKnownFaces(encodings)
while True:
    ret , frame = vid.read()
    if ret == True:
        if count % 60 == 0:
            detectAllFaces(frame,faces,encodings)
        else :
            drawAllFaces(frame , faces)
        count += 1
        cv2.imshow('' , frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
