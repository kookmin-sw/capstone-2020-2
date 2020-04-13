from .models import *
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .customLogin import *
import random, os, pickle
from PIL import Image

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
path = os.path.join(BASE_DIR, 'media')

@api_view(['POST'])
def signup(request, format=None):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save new user to db.
        newUser = User.objects.create_user(username=serializer.data['username'], userFace=request.FILES['userFace'])
        newUser.save()
        payload = {
            'id': newUser.id,
            'username': newUser.username,
        }

        # Check if the picture can be encoded
        imgPath = os.path.join(path, str(newUser.userFace))
        try:
            img = face_recognition.load_image_file(imgPath)
            login_face_encoding = face_recognition.face_encodings(img)[0]
        except IndexError:
            return HttpResponse("Please take another picture.", status=409)

        # Save encoded image of user.
        current_dir = os.getcwd()
        userInfo = [(newUser.id, newUser.username), login_face_encoding]
        if 'encoded_users' not in os.listdir(current_dir):
            with open('encoded_users', "wb") as fw:
                pickle.dump(userInfo, fw)
                fw.close()
        else:
            with open('encoded_users', "ab") as fi:
                pickle.dump(userInfo, fi)
                fi.close()

        return JsonResponse(payload)

    # TODO : validate user

@api_view(['GET','POST'])
def login(request, format=None):
    if request == 'GET':

        users = User.objects.all()
        numpyUsersList = []
        if users.exists():
            for user in users:
                imagePath = os.path.join(path, str(user.userFace))
                userImage = face_recognition.load_image_file(imagePath)
                numpyUsersList.append([(user.id, user.username), asarray(userImage)])

        capture = cv2.VideoCapture(0)
        capture.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)

        while True:
            ret, frame = capture.read()

            if not ret:
                break

            try:
                login_face_encoding = face_recognition.face_encodings(frame)[0]
                break
            except IndexError:
                return HttpResponse("Please stay closer to the camera.", status=status.HTTP_404_NOT_FOUND)

        # TODO : Save encoded userface in static file (pickle)

        user_images_encoding = []
        for each in numpyUsersList:
            encoding_image = face_recognition.face_encodings(each[1])[0]
            user_images_encoding.append(encoding_image)

        matches = face_recognition.compare_faces(user_images_encoding, login_face_encoding)
        face_distances = face_recognition.face_distance(user_images_encoding, login_face_encoding)

        if not True in matches:
            return HttpResponse("Please sign up first", status=status.HTTP_409_CONFLICT)
        else:
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                matched_user = numpyUsersList[best_match_index][0]
                payload = {
                    'id': matched_user[0],
                    'username': matched_user[1],
                }
                return JsonResponse(payload)
            else:
                return HttpResponse("Please sign up first", status=status.HTTP_409_CONFLICT)

class getAnalyzingVideo(APIView):
    def get(self, request, id):

        # TODO : Filter already seen videos using sessions.

        max_id = Video.objects.all().aggregate(max_id=Max('videoId'))['max_id']
        while True:
            randId = random.randint(1, max_id)
            video = Video.objects.filter(pk=randId).first()
            if video:
                return JsonResponse({
                    'user' : id,
                    'link' : video.link,
                    'startTime' : video.startTime,
                    'duration' : video.duration,
                    'tag' : video.tag,
                })