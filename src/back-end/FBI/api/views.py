from .models import *
from django.db.models import Max
from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
import random
from numpy import asarray
import cv2
import face_recognition
import numpy as np
import os

@api_view(['POST'])
def signup(request, format=None):
     if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET','POST'])
def login(request, format=None):
    if request == 'GET':
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.path.join(BASE_DIR, 'media')

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