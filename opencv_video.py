from sqlite3 import Timestamp
from turtle import stamp
import face_recognition
import cv2
import json
import requests
import datetime

from firebase import firebase
person_face_encodings = []
person_face_names = []

isCheck = False


cap = cv2.VideoCapture(r'Video/ryan.mp4',0)
face_recognitions = []
frameProcess = True

#เชื่อมต่อฐานข้อมูล
firebase = firebase.FirebaseApplication('https://comicservices-37ded-default-rtdb.firebaseio.com/', None)
result = firebase.get('/person/', '')
for person in result:
    jsn = requests.get('https://comicservices-37ded-default-rtdb.firebaseio.com/person.json')
    data = jsn.json()
    database_image = face_recognition.load_image_file('image/'+data[person]['image'])
    data_base_encoding = face_recognition.face_encodings(database_image)[0]
    person_face_names.append(data[person]['Name'])
    person_face_encodings.append(data_base_encoding)

while True:
    ret, frame = cap.read()
    rgb_resizing = frame[:, :, ::-1]
    if frameProcess:
        data_locations = face_recognition.face_locations(rgb_resizing)
        data_encodings = face_recognition.face_encodings(rgb_resizing, data_locations)
        data_names = []
        for dc in data_encodings:
            matches = face_recognition.compare_faces(person_face_encodings, dc)
            name = "UNKNOWN"
            if True in matches:
                first_match_index = matches.index(True)
                name = person_face_names[first_match_index]

                #check name
                if(isCheck == False):
                    data_check =  { 
                        'Name': name,
                        'TIME': datetime.datetime.now()
                        }
                    result = firebase.post('/checkIn',data_check)
                    isCheck = True
                
            data_names.append(name)
    frameProcess = not frameProcess
    for top, right, bottom, left in data_locations:
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 4)
        data_encodings = face_recognition.face_encodings(rgb_resizing, data_locations)
        data_names = []
        for dc in data_encodings:
            matches = face_recognition.compare_faces(person_face_encodings, dc)
            name = "UNKNOWN"
            if True in matches:
                first_match_index = matches.index(True)
                name = person_face_names[first_match_index]
            data_names.append(name)
            cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (26, 174, 10), cv2.FILLED)
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
    frame = cv2.resize(frame, (600, 340))
    cv2.imshow('Video', frame)
    if cv2.waitKey(25) == 13:
        data = {'Name': name,
                'Time': datetime.datetime.now()
                }
        result = firebase.post('/checkOut',data)
        break
cap.release()
cv2.destroyAllWindows()