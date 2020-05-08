import requests
import json

def predict_emotion(image)):
    # 결제한 다음에 아래 key 값 바꿔줘야 함.
    # Key
    subscription_key = "93d41a68c59b4e19b350ddf7fd5fd5a5"
    # Endpoint
    base_uri = "https://koreacentral.api.cognitive.microsoft.com"

    '''
    with open(image_path, 'rb') as f:
        image_data = f.read()
    '''
    image_data = image      # 이거 저장되어 있는 파일로만 보내야됐나 그랬던 것 같은데.. 일단 돌려봐야 할 듯.
    # header 설정
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key,
    }

    # parameter 설정
    params = {
        'returnFaceId': 'true',
        'returnFaceLandmarks': 'false',
        'returnFaceAttributes': 'smile,emotion',
    }

    # 리퀘스트 요청
    response = requests.request('POST', base_uri + '/face/v1.0/detect', json=None, data=image_data, headers=headers, params=params)
    emotion_dicts = response.json()[0]['faceAttributes']['emotion']
    '''
    # 가장 높은 확률 순으로 정렬
    emotion_dicts = sorted(emotion_dicts.items(), reverse=True, key=lambda x:x[1])
    # 예측한 감정 중 가장 높은 것 3 개를 가져옴.
    first, second, third = emotion_dicts[0][0], emotion_dicts[1][0], emotion_dicts[2][0]
    '''
    emotions = emotion_dicts.items()      # anger, contempt, disgust, fear, happiness, neutral, sadness, surprise

    # return (first, second, third)
    return emotions