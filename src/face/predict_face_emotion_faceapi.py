import cv2
import base64
import requests
import json
import numpy as np
import os

BASE_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))
xmlPath = os.path.join(BASE_DIR, 'src/face/haarcascade_frontalface_default.xml')

def predict_emotion(image_path):
    # Key
    subscription_key = "ac039e4790244804a34be1b1afa4e4ee"
    # Endpoint
    endpoint = "https://capstone-faceapi.cognitiveservices.azure.com/"
    base_uri = "https://koreacentral.api.cognitive.microsoft.com"

    face_cascade = cv2.CascadeClassifier(xmlPath)
    
    image = cv2.imread(image_path)

    # face detection 을 위해 흑백으로 변환
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_BGR2GRAY)

    # face detection
    faces = face_cascade.detectMultiScale(gray, 1.1, 4)
    
    # 사진에 얼굴이 있는 경우
    if len(faces):
        buffer = cv2.imencode('.jpg', image)[1].tostring()
        '''
        with open(image_path, 'rb') as f:
            image_data = f.read()
        '''

        # header 설정
        headers = {
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': subscription_key,
        }

        # parameter 설정
        params = {
            'returnFaceId': 'true',
            'returnFaceLandmarks': 'false',
            'returnFaceAttributes': 'emotion',
        }

        # 리퀘스트 요청
        response = requests.request('POST', base_uri + '/face/v1.0/detect', json=None, data=buffer, headers=headers, params=params)
        emotion_dicts = response.json()[0]['faceAttributes']['emotion']
        print(emotion_dicts)

        emotions = list(emotion_dicts.items())
        emotions = [e[1] for e in emotions]
        
        return True, emotion_dicts
    
    # 사진에 얼굴이 없는 경우.
    else:
        return False, None