from deepface import DeepFace
from unittest import result
from firebase import firebase

firebase = firebase.FirebaseApplication('https://comicservices-37ded-default-rtdb.firebaseio.com/', None)
data = {'Name': 'ryan',
        'Surname': 'Gosling',
        'Gender': 'M',
        'image': 'ryan.jpg'}
result = firebase.post('/person',data)
print(result)

result = DeepFace.analyze(img_path = "jaimg.jpg")
print("Emotion:", result["emotion"])
print("Dominant Emotion:", result["dominant_emotion"])