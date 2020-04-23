import face_recognition
import numpy as np

# 로그인 함수
# 사용자 이미지랑, 유저 목록 리스트 [(uid_1, 이미지_1), (uid_2, 이미지_2), ... ] 를 넘겨받음.
# 등록된 유저면 uid 리턴
# 등록되지 않은 유저면 None 값을 리턴
def login(login_face, user_list, threshold):
    """Face Login Function
    
    Arguments:
        login_face {opencv image format} -- 로그인 하려는 사용자의 얼굴 이미지
        user_list {[(uid, opencv image format), ...]} -- DB 에서 불러온 기존 유저들의 uid 와 인코딩 이미지 쌍 리스트
        threshold {float} -- 매칭되는 얼굴과의 distance 차이. 이 값보다 작으면 매칭된다고 판단하는 것.
    
    Returns:
        string -- 등록된 유저이면 uid, 등록되지 않은 유저이면 None 값 리턴
    """

    # user_list 가 빈 리스트면 None 리턴
    if not user_list:
        return None

    login_face_encoding = face_recognition.face_encodings(login_face, num_jitters=10, model="large")[0]

    # 전달받은 (uid, 인코딩 이미지) 리스트에서 이미지만 따로 분리
    user_images_encoding = []
    for user in user_list:
        user_images_encoding.append(user[1])

    matches = face_recognition.compare_faces(user_images_encoding, login_face_encoding, threshold)
    face_distances = face_recognition.face_distance(user_images_encoding, login_face_encoding)
    print("Distance :", face_distances)     # 로그인 하려는 사람의 얼굴과, 등록된 전체 회원들의 얼굴 별 유사도 거리를 출력
    
    # 유저 리스트에 매칭되는 사람이 없을 경우
    if not True in matches:
        return None
    # 유저 리스트에 매칭되는 사람이 있을 경우
    else:
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            matched_uid = user_list[best_match_index][0]
            return matched_uid
        else:
            return None