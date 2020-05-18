from .models import *
from django.db.models import Max
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .customLogin import *
import random, os, pickle, sys
from datetime import datetime
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))))
from src.face.predict_face_emotion_faceapi import predict_emotion

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Directory path for saving real-time data.
dirPath = os.path.join(ROOT_DIR, 'FBI-data')
dataDirPath = ''
# Path for saving userFace images.
path = os.path.join(BASE_DIR, 'media')
# Temporarily save encoded image of new user for signup.
encodedImage = []

@api_view(['POST'])
def signup(request):
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
        # Create data directory for saving real-time data.
        # Path : capstone-2020-2/FBI-data
        if not os.path.isdir(dirPath):
            os.mkdir(dirPath)
        # Create subdirectory for user.
        dataDirPath = os.path.join(dirPath, newUser.userFace.name.split("/")[1].split(".")[0])
        if not os.path.isdir(dataDirPath):
            os.mkdir(dataDirPath)
        return JsonResponse(payload)
    else:
        return Response(serializer.errors)

@api_view(['POST'])
def login(request):
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
        # Set user data directory path.
        global dataDirPath
        dataDirPath = os.path.join(dirPath, '{}_{}'.format(user[1], user[0]))
        payload = {
            'id': user[0],
            'username': user[1],
        }
        return JsonResponse(payload)

@api_view(['POST'])
def logout(request):
    try:
        #del request.session['id']
        request.session.flush()
    except KeyError:
        pass
    global dataDirPath
    dataDirPath = ''
    return HttpResponse("You're logged out.")

class getAnalyzingVideo(APIView):
    def get(self, request, id, emotionTag):
        viewed_video_list = request.session.get('viewed_videos', [])
        # Todo: Get random videoId which is in filtered emotion
        max_id = Video.objects.filter(tag=emotionTag).aggregate(max_id=Max('videoId')).get('max_id')
        print(max_id)
        print(request)
        if max_id is None:
            return HttpResponse("No videos.")
        if request.session.get('viewed_videos') and Video.objects.count() == len(request.session.get('viewed_videos')):
            return HttpResponse("Seen every videos.", status=status.HTTP_404_NOT_FOUND)
        while True:
            randId = random.randint(1, max_id)
            # Check if the video is in viewed video session list.
            if randId in viewed_video_list:
                continue
            video = Video.objects.filter(pk=randId).first()
            if video:
                print("hohohohoho")
                viewed_video_list.append(randId)
                request.session['viewed_videos'] = viewed_video_list
                request.session.modified = True
                # Create subdirectory for played videos.
                videoInfo = '{}_{}'.format(video.title, video.videoId)
                global dataDirPath
                print("error33333333333333333")
                videoDirPath = os.path.join(dataDirPath, videoInfo)
                if not os.path.isdir(videoDirPath):
                    print("error....")
                    os.makedirs(videoDirPath)
                    print("no..............")
                # Create directories based on the datetime the video was played
                # since each video might be played multiple times.
                dateDirPath = os.path.join(videoDirPath, datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                os.mkdir(dateDirPath)
                # Create directories separately for face, eeg data.
                os.mkdir(os.path.join(dateDirPath, 'face'))
                os.mkdir(os.path.join(dateDirPath, 'eeg'))
                return JsonResponse({
                    'user' : id,
                    'link' : video.link,
                    'id' : video.videoId,
                    'startTime' : video.startTime,
                    'duration' : video.duration,
                    'tag' : video.tag,
                    'imgPath': os.path.join(dateDirPath, 'face'),
                })
            else:
                continue
    def post(self, request, id, emotionTag):
        return HttpResponseRedirect(reverse('realTimeResult'))

@api_view(['POST'])
def realTimeAnalyze(request, id):
    img = Image.open(request.FILES['image'])
    # Save image to corresponding dir path.
    imgName = request.data['image'].name
    imgPath = os.path.join(request.data['imgPath'], imgName)
    img.save(imgPath, "JPEG")
    # predictResult = predict_emotion(imgPath)
    # print(predictResult)
    # TODO : Get results from Main Program 2 (analyzing module).

    emotionTag = 'happy'
    emotionValues = {
        'happy': random.random(),
        'sad': random.random(),
        'disgust': random.random(),
        'contempt': random.random(),
        'surprise': random.random(),
        'fear': random.random(),
        'neutral': random.random(),
    }
    payload = {
        'emotionTag': emotionTag,
        'emotionValues': emotionValues
    }
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
    return JsonResponse(payload)