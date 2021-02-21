import face_recognition

class Face:
    def __init__(self , location , name ):
        self.name = name
        self.location = location

    def isFaceInFrame(self , frame):
            top , right , bottom , left = self.location
            newFrame = frame[top - 40 : bottom + 40 , left - 40 : right + 40 , : ]
            newLocation = face_recognition.face_locations(newFrame)
            if len(newLocation) == 0:
                return False
            newLocation = newLocation[0]
            self.location = (newLocation[0] + top - 40 , left - 40 + newLocation[1]  , top - 40 + newLocation[2] ,newLocation[3] + left - 40)
            return True
