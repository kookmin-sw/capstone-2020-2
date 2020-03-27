import face_recognition
import cv2
import numpy as np
import os
# import pickle

'''
def prepare_known_faces(known_faces_path):
    # 회원 별 얼굴 사진이 있는 dir
    dirs = os.listdir(known_faces_path)

    known_faces = []
    known_face_names = []
    
    # dir 별로 한 사람씩...
    for face_image_name in dirs:        
        person_name = face_image_name.split('.')[0]
        image_path = known_faces_path + "/" + face_image_name

        known_image = face_recognition.load_image_file(image_path)
        known_image_encoding = face_recognition.face_encodings(known_image)[0]

        known_faces.append(known_image_encoding)
        known_face_names.append(person_name)
        
    return known_faces, known_face_names
'''

def add_new_person(new_person_image):
    # known_faces.append(new_person_image)
    new_person_name = input("Enter your name : ")       ######## 여기가 웹에서 입력한 이름이랑 연결되어야 함 ㅇㅇㅇ
    
    # DB 에 새로운 유저 튜플을 만들어 추가
    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO User(username, userFace) VALUES (%s, %s)', (new_person_name, new_person_image))
    mysql.connection.commit()
    cur.close()
    
    '''
    known_face_names.append(new_person_name)
    with open('known_faces_list.txt', 'wb') as f:
        pickle.dump(known_faces, f)
        f.close()
    with open('known_face_names_list.txt', 'wb') as f:
        pickle.dump(known_face_names, f)
        f.close()
    '''
    print(f"Added a new user : {new_person_name}")
    # print(known_face_names)


# 로그인 함수
def login():
    '''
    # 유저 목록 이진파일이 있는지 없는지 확인.
    current_dir = os.getcwd()
    # 없다면 소프트웨어가 처음으로 시작된 것.
    # prepare_known_faces() 함수 실행 필요.
    if "known_faces_list.txt" not in os.listdir(current_dir):
        print("No User Data")
        print("Loading user data...")
        known_faces, known_face_names = prepare_known_faces("known_faces")
        with open('known_faces_list.txt', 'wb') as f:
            pickle.dump(known_faces, f)
            f.close()
        with open('known_face_names_list.txt', 'wb') as f:
            pickle.dump(known_face_names, f)
            f.close()

    with open('known_faces_list.txt', 'rb') as known_faces_list:
        with open('known_face_names_list.txt', 'rb') as known_face_names_list:
            known_faces = pickle.load(known_faces_list)
            known_face_names = pickle.load(known_face_names_list)
            print(known_face_names)     # 현재 등록된 회원들의 이름을 출력
            '''
    # DB 등록되어 있는 회원들의 얼굴 사진을 불러오기.
    cur = mysql.connection.cursor()
    cur.execute('SELECT userFace from User')
    user_list = cur.fetchall()
    cur.close()

    camera = cv2.VideoCapture(0)
    frame = camera.read()[1]
    
    # unknown_image_path = input("Enter a test image : ")         ###### 이건 로그인 하려는 사람의 얼굴 사진인데... 지금은 임의의 파일 경로를 넣어주는 식.
                                                                ###### 이게 웹캠으로 찍고 있는 사람의 얼굴 캡쳐 사진이 되어야 한다 ㅇㅇㅇ
    # unknown_image = face_recognition.load_image_file(unknown_image_path)
    # unknown_face_encoding = face_recognition.face_encodings(unknown_image)[0]
    unknown_face_encoding = face_recognition.face_encodings(frame)[0]

    matches = face_recognition.compare_faces(known_faces, unknown_face_encoding)
    face_distances = face_recognition.face_distance(known_faces, unknown_face_encoding)
    print("Distance :", face_distances)     # 로그인 하려는 사람의 얼굴과, 등록된 전체 회원들의 얼굴 별 유사도 거리를 출력
    
    # 등록된 회원들 중, 매칭되는 사람이 없다고 판단되면...
    # 처음 보는 유저라고 알려주고 회원가입 여부를 물음.
    if not True in matches:
        print("I've never seen you before.")
        sign_up = input("Would you like to sign up? (Y / N) : ")        ###### 웹이라면 이게 회원가입을 하겠냐?? 에 대한 답으로 들어와야 함.
        ###### 답이 등록하겠다 (여기서는 y, Y) 면 add_new_person() 함수를 호출 ㅇㅇㅇ
        if sign_up in ['y', 'Y']:
            # add_new_person(unknown_face_encoding, known_faces, known_face_names)
            add_new_person(unknown_face_encoding)
    # 등록된 회원들 중, 매칭되는 사람이 있을 경우.
    else:
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            matched_face = user_list[best_match_index]
        
        # DB 에서 매칭되는 얼굴 정보로 회원의 이름 읽어오기.
        cur = mysql.connection.cursor()
        cur.execute('SELECT username from User WHERE userFace = %s', (matched_face))
        username = cur.fetchone()
        cur.close()
        print("You are", username)
            # known_face_names_list.close()
        # known_faces_list.close()

if __name__ == '__main__':
    login()