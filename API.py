from Face import Face
import face_recognition
import cv2
import os

def rectangle(img , top , right , bottom , left): # The method gets 4 points and draws a rectangle at these points
    if img.ndim == 2:
        img[bottom - 20: bottom + 20, left - 1: right + 1] = 255
        img[top - 1 : top + 1 , left : right] = 255
        img[top - 1: bottom + 1, right - 1: right + 1] = 255
        img[top - 1 : bottom + 1 , left - 1 : left + 1] = 255
    else :
        rectangle(img[:,:,0],top,right,bottom,left)
        rectangle(img[:,:,1], top, right, bottom, left)
        rectangle(img[:,:,2], top, right, bottom, left)


def detectAllFaces(frame , faces , encodings): #scan the entire frame for detect new faces.
    newFaces = []
    for location in face_recognition.face_locations(frame):
        newFace = Face(location, '')
        name = lookForFace(location , faces)
        if len(name) > 0:
            newFace.name = name
        else:
            newFace.name = getName(frame,location,encodings)
        newFaces.append(newFace)
    faces[:] = newFaces[:]


def lookForFace(face , faceList): #get face location and list of faces locations, and compare that face location with the other locations on the list
    for f in faceList:
        if isFaceinRectangle(face , getRectangleLocation(f.location , 40)):
            return f.name
    return ''


def drawAllFaces(frame , faces): #get faces locations and draw rectangle around them
    i = 0
    for face in faces:
        prevLocation = getRectangleLocation(face.location , 20)
        if face.isFaceInFrame(frame):
            if isFaceinRectangle(face.location , prevLocation):
                face.location = getRectangleLocation(prevLocation , -20)
                rectangle(frame, prevLocation[0] , prevLocation[1], prevLocation[2] , prevLocation[3])
                cv2.putText(frame,face.name , (face.location[3] , face.location[2] + 30) , cv2.FONT_HERSHEY_SIMPLEX , 0.6 , 2 )
        i+=1

def getRectangleLocation(location , padding): #get location and padding and return new location with the given margin
    return (location[0] - padding , location[1] + padding , location[2] + padding , location[3] - padding)

def isFaceinRectangle(faceLocation , recLocation): #check if the rectangle location contain the face location
    return faceLocation[0] > recLocation[0] and faceLocation[1] < recLocation[1] and faceLocation[2] < recLocation[2] and faceLocation[3] > recLocation[3]


def getAllKnownFaces(encodings): #scan the faces reposatory and get theirs encodings and names
    list = os.listdir(os.path.abspath(os.getcwd()))
    for path in list:
        pathSplit = path.split('.')
        ext = pathSplit[len(pathSplit) - 1]
        if ext == 'jpg' or ext == 'jpeg':
            img = face_recognition.load_image_file(path)
            encodings.append([face_recognition.face_encodings(img)[0],pathSplit[0]])

def getName(frame , location , encodings): #comapre face with the list of encodings. if the face is exist, return the name
    knownFace = face_recognition.face_encodings(frame , [location])
    for encon in encodings:
        if face_recognition.compare_faces(knownFace , encon[0])[0]:
            return encon[1]
    return 'unknwon'

