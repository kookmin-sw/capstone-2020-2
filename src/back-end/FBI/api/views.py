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
        newUser = User.objects.create_user(username=serializer.data['username'],
                                           userFace=request.FILES['userFace'])
        newUser.save()
        payload = {
            'id': newUser.id,
            'username': newUser.username,
        }

        # Check if the picture can be encoded
        imgPath = os.path.join(path, str(newUser.userFace))
        try:
            img = face_recognition.load_image_file(imgPath)
            login_face_encoding = face_recognition.face_encodings(img, num_jitters=10, model="large")[0]
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
            # Validate user is a newcomer.
            encodeUsers = getEncodedUsersList()
            user = isUser(login_face_encoding, encodeUsers)
            if user is not None:
                os.remove(os.path.join(path, str(newUser.userFace)))
                User.objects.filter(id=newUser.id).delete()
                return HttpResponse("You already have an account", status=status.HTTP_409_CONFLICT)
            # Add encoded image if new user.
            with open('encoded_users', "ab") as fi:
                pickle.dump(userInfo, fi)
                fi.close()

        return JsonResponse(payload)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def login(request, format=None):
    img = Image.open(request.FILES['userFace'])
    imgPath = os.path.join(BASE_DIR, 'temp.jpg')
    img.save(imgPath, 'JPEG')

    try:
        img = face_recognition.load_image_file(imgPath)
        login_face_encoding = face_recognition.face_encodings(img, num_jitters=10, model="large")[0]
        os.remove(imgPath)
    except IndexError:
        return HttpResponse("Please take another picture.", status=409)

    encodeUsers = []
    with open('encoded_users', 'rb') as fr:
        while True:
            try:
                encodeUsers.append(pickle.load(fr))
            except EOFError:
                break

    user = isUser(login_face_encoding, encodeUsers)
    if user is None:
        return HttpResponse("Please sign up first", status=status.HTTP_409_CONFLICT)
    else:
        payload = {
            'id': user[0],
            'username': user[1],
        }
        return JsonResponse(payload)

# TODO : Logout
'''
@api_view(['POST'])
def logout(request, format=None):
'''

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