import face_recognition
import numpy as np
import pickle

def getEncodedUsersList():
    encodeUsers = []
    with open('encoded_users', 'rb') as fr:
        while True:
            try:
                encodeUsers.append(pickle.load(fr))
            except EOFError:
                break
    return encodeUsers

def isUser(login_face_encoding, encodedUsers):
    user_images_encoding = []
    for user in encodedUsers:
        user_images_encoding.append(user[1])

    matches = face_recognition.compare_faces(user_images_encoding, login_face_encoding)
    face_distances = face_recognition.face_distance(user_images_encoding, login_face_encoding)

    if not True in matches:
        return None
    else:
        best_match_index = np.argmin(face_distances)
        if matches[best_match_index]:
            matched_user = encodedUsers[best_match_index][0]
            return matched_user
        else:
            return None