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
# Temporarily save encoded image of new user for signup.
encodedImage = []

@api_view(['POST'])
def signup(request, format=None):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        # Save new user to db.
        newUser = User.objects.create_user(username=serializer.data['username'],
                                           userFace='default')
        newUser.save()
        # Update userFace file name.
        newUser.userFace = request.FILES['userFace']
        newUser.save()
        payload = {
            'id': newUser.id,
            'username': newUser.username,
        }

        # Save encoded image of user.
        current_dir = os.getcwd()
        userInfo = [(newUser.id, newUser.username), encodedImage[0]]
        del encodedImage[0]
        if 'encoded_users' not in os.listdir(current_dir):
            with open('encoded_users', "wb") as fw:
                pickle.dump(userInfo, fw)
                fw.close()
        else:
            with open('encoded_users', "ab") as fi:
                pickle.dump(userInfo, fi)
                fi.close()
        request.session['id'] = newUser.id
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
        return HttpResponse("Please take another picture.", status=status.HTTP_409_CONFLICT)

    current_dir = os.getcwd()
    if 'encoded_users' not in os.listdir(current_dir):
        encodedImage.append(login_face_encoding)
        return HttpResponse("First user.", status=status.HTTP_406_NOT_ACCEPTABLE)

    encodeUsers = []
    with open('encoded_users', 'rb') as fr:
        while True:
            try:
                encodeUsers.append(pickle.load(fr))
            except EOFError:
                break

    user = isUser(login_face_encoding, encodeUsers)
    if user is None:
        encodedImage.append(login_face_encoding)
        return HttpResponse("Please sign up first", status=status.HTTP_404_NOT_FOUND)
    else:
        request.session['id'] = user[0]
        payload = {
            'id': user[0],
            'username': user[1],
        }
        return JsonResponse(payload)

@api_view(['POST'])
def logout(request, format=None):
    try:
        #del request.session['id']
        request.session.flush()
    except KeyError:
        pass
    return HttpResponse("You're logged out.")

class getAnalyzingVideo(APIView):
    def get(self, request, id):
        viewed_video_list = request.session.get('viewed_videos', [])
        max_id = Video.objects.all().aggregate(max_id=Max('videoId'))['max_id']
        if max_id is None:
            return HttpResponse("No videos.")
        if Video.objects.count() == len(request.session['viewed_videos']):
            return HttpResponse("Seen every videos.", status=status.HTTP_404_NOT_FOUND)
        while True:
            randId = random.randint(1, max_id)
            # Check if the video is in viewed video session list.
            if randId in viewed_video_list:
                continue
            else:
                video = Video.objects.filter(pk=randId).first()
                if video:
                    viewed_video_list.append(randId)
                    request.session['viewed_videos'] = viewed_video_list
                    request.session.modified = True
                    return JsonResponse({
                        'user' : id,
                        'link' : video.link,
                        'startTime' : video.startTime,
                        'duration' : video.duration,
                        'tag' : video.tag,
                    })

class getTrialVideo(APIView):
    def get(self, request, id, emotionTag):

        # TODO : Filter already seen videos using sessions.

        max_id = Video.objects.filter(tag=emotionTag).aggregate(max_id=Max('videoId'))['max_id']
        if max_id is None:
            return HttpResponse("No videos.")

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

class realTimeAnalyze(APIView):
    def get(self, request, id):
        image = request.FILES['image']

        # Pass image to face analyze model.
        # methodName(image)

        # Retrieve result and send to FE.
        # result = []
        # while True:
        #   result = methodName()
        #   if result is not None:
        #       break
        # emotionTag = result[0]
        # emotionValues = result[1]
        # eegConnections = result[2]
        # payload = {
        #       "emotionTag" : emotionTag,
        #       "emotionValues" : {
        #           "happy" : emotionValues[0],
        #           "angry" : ....
        #       },
        #       "eegConnections" : {
        #           "eeg1" : 1,
        #           "eeg2" : 1,
        #           "eeg3" : 1,
        #           "eeg4" : 1,
        #           "eeg5" : 1,
        #           "eeg6" : 1,
        #           "eeg7" : 1,
        #           "eeg8" : 1,
        #       },
        # }

        # TODO
        # Cache retrieved results & Save in DB at once.

        # return JsonResponse(payload)