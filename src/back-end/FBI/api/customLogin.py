import face_recognition
import numpy as np
from numpy import asarray
from .models import User

def getUsersList():
    '''Returns list holding users' image converted to numpy array.'''
    users = User.objects.all()
    numpyUsersList = []

    if users.exists():
        for user in users:
            numpyUsersList.append([(user.id, user.username), asarray(user.userFace)])

    return numpyUsersList

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