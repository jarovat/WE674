import json
import requests

from firebase import firebase

firebase = firebase.FirebaseApplication('https://comicservices-37ded-default-rtdb.firebaseio.com/' , None)
result = firebase.get('/person/', '')
for person in result:
    jsn = requests.get('https://comicservices-37ded-default-rtdb.firebaseio.com/person.json')
    data = jsn.json()
    print(data[person]['Name'])
    print(data[person]['Surname'])
    print(data[person]['image'])
    print(data[person]['Gender'])