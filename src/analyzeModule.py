from src.analyze.eeg.eegAnalyzeModule import *
from src.analyze.face.predict_face_emotion_faceapi import *
import operator

def prob_distribution_method(dic):
    total = sum(list(dic.values()))
    for key, val in dic.items():
        dic[key] /= total
    return dic

def multimodal_emotion(face_emotions, face_detected, eeg_emotions, n_railed, high_enhance=3, low_enhance=1):
    unused_emotions = ["anger", "contempt", "surprise"]
    
    if face_detected:
        for emo in unused_emotions:
            del face_emotions[emo]
        max_face_emotions = max(face_emotions.items(), key=operator.itemgetter(1))[0]
        
    # 둘다없음
    if n_railed > 0 and not face_detected:
        return None, None
    
    # 얼굴만 감지
    elif face_detected and n_railed > 0:
        emotions = face_emotions
        
    # 센서만 감지
    elif not face_detected and n_railed == 0:
        emotions = eeg_emotions
    
    # 둘다 감지
    else:
        # EEG 값이 스트링인 경우
        if isinstance(eeg_emotions, str):
            enhance = high_enhance if max_face_emotions == "neutral" else low_enhance
            face_emotions[eeg_emotions] *= enhance    # 이 값만큼 eeg 결과 감정에 가중치를 줌.
            emotions = prob_distribution(face_emotions)    # 확률값으로 만들어주기.
        # EEG 값이 확률값인 경우
        else:
            # 무표정일 때
            if max_face_emotions == "neutral":
                for key, val in face_emotions.items():
                    face_emotions[key]  += (low_enhance*face_emotions[key] + high_enhance*eeg_emotions[key])
            if max_face_emotions == "neutral":
                for key, val in face_emotions.items():
                    face_emotions[key]  += (high_enhance*face_emotions[key] + low_enhance*eeg_emotions[key])
            emotions = prob_distribution_method(face_emotions)
        return max_face_emotions, emotions

def detectEmotion(facePath, eegPath, RM):
    face_detected, face_emotion = predict_emotion(facePath)
    eeg_emotion, n_railed, sensor_status = predict_emotion_EEG(model, eegPath, chosen_channels, freqs, sf=256)
    # RM =========================================================
    eeg_emotion[RM] *= 3    # 이 값만큼 eeg 결과 감정에 가중치를 줌.
    eeg_emotion = prob_distribution_method(eeg_emotion)
    # ============================================================
    emotion, prob_distribution = multimodal_emotion(face_emotion, face_detected, eeg_emotion, n_railed)
    return emotion, prob_distribution, sensor_status