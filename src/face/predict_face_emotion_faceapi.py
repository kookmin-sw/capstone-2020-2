import requests
import json

def predict_emotion(image):
    # 얘네 두 개는 상수로 밖에 빼놔도 괜찮을 듯... 아니면 말고...
    # Key
    subscription_key = "ac039e4790244804a34be1b1afa4e4ee"
    # Endpoint
    endpoint = "https://capstone-faceapi.cognitiveservices.azure.com/"
    base_uri = "https://koreacentral.api.cognitive.microsoft.com"
    
    '''
    with open(image_path, 'rb') as f:
        image_data = f.read()
    '''
    image_data = image
    
    print(f"image_data 타입 : {type(image_data)}")
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
    response = requests.request('POST', base_uri + '/face/v1.0/detect', json=None, data=image_data, headers=headers, params=params)
    emotion_dicts = response.json()[0]['faceAttributes']['emotion']

    '''
    emotions = list(emotion_dicts.items())
    emotions = [e[1] for e in emotions]
    
    return emotions
    '''
    return emotion_dicts