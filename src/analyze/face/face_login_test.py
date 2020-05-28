from face_login import login
import os
import pickle
import face_recognition
import cv2

# 유저 목록 이진파일이 있는지 없는지 확인.
current_dir = os.getcwd()

if "user_list.txt" not in os.listdir(current_dir):
    print("No User Data.")
    user_list = []
else:
    user_list_file = open('user_list.txt', 'rb')
    user_list = pickle.load(user_list_file)
    user_list_file.close()
    user_name_list = []
    for user in user_list:
        user_name_list.append(user[0])
    print("---------- User List ----------")
    print(len(user_name_list))
    print(user_name_list)

user_image_path = input("Enter a User image path : ")
user_image = cv2.imread(user_image_path)

uid = login(user_image, user_list, 0.4)

if uid is None:
    print("You're Not on the user list.")
    answer = input("Would you like to sign up? (Y / N) : ")

    if answer in ['y', 'Y']:
        user_image_encoding = face_recognition.face_encodings(user_image, num_jitters=10, model="large")[0]
        uid = input("Enter the your name : ")
        user_list.append([uid, user_image_encoding])
        user_list_file = open('user_list.txt', 'wb')
        pickle.dump(user_list, user_list_file)
        user_list_file.close()
else:
    print(f"Hello, {uid} !")