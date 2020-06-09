from .models import *
from django.db.models import Count
from django.utils import timezone
from django.urls import reverse
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from . import serializers
from .customLogin import *
import random, os, pickle, sys, shutil
from PIL import Image

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))))))))
# from src.analyze.face.predict_face_emotion_faceapi import predict_emotion
from src.analyzeModule import detectEmotion

ROOT_DIR = os.path.dirname(os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(
    os.path.abspath(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))))))))
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Directory path for saving real-time data.
dirPath = os.path.join(ROOT_DIR, 'FBI-data')
dataDirPath = ''
dateDirPath = ''
# Path for saving userFace images.
path = os.path.join(BASE_DIR, 'media')
# Temporarily save encoded image of new user for signup.
encodedImage = []
# Dict for saving accumulated real time data.
resultsDic = {}

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
        global dataDirPath
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
        request.session.flush()
    except KeyError:
        pass
    global dataDirPath
    dataDirPath = ''
    return HttpResponse("You're logged out.")

class getAnalyzingVideo(APIView):
    def get(self, request, id, emotionTag):
        viewedVideos = request.session.get('viewedVideos', {})
        if emotionTag not in viewedVideos:
            viewedVideos[emotionTag] = []
        videoObjects = Video.objects.filter(tag=emotionTag)
        numOfVideos = videoObjects.aggregate(count=Count('videoId')).get('count')
        videos = videoObjects.values_list('videoId', flat=True)
        if numOfVideos == 0:
            return HttpResponse("No videos.")
        if len(viewedVideos[emotionTag]) == numOfVideos:
            return HttpResponse("You've seen every video.", status=status.HTTP_404_NOT_FOUND)
        while True:
            randId = random.sample(list(videos), 1)[0]
            if randId in viewedVideos[emotionTag]:
                continue
            video = Video.objects.filter(pk=randId).first()
            if video:
                viewedVideos[emotionTag].append(randId)
                request.session['viewedVideos'] = viewedVideos
                request.session.modified = True
                # Create subdirectory for played videos.
                videoInfo = '{}_{}'.format(video.title, video.videoId)
                global dataDirPath
                videoDirPath = os.path.join(dataDirPath, videoInfo)
                if not os.path.isdir(videoDirPath):
                    os.makedirs(videoDirPath)
                # Create directories based on the datetime the video was played
                # since each video might be played multiple times.
                global dateDirPath
                now = timezone.localtime()
                dateDirPath = os.path.join(videoDirPath, now.strftime('%Y-%m-%d %H:%M:%S'))
                os.mkdir(dateDirPath)
                # Create directories separately for face, eeg data.
                os.mkdir(os.path.join(dateDirPath, 'face'))
                os.mkdir(os.path.join(dateDirPath, 'eeg'))
                # Save result
                result = Result.objects.create(user=User.objects.filter(pk=id).first(),
                                               video=Video.objects.filter(pk=randId).first(),
                                               viewedDate=now,
                                               dataPath=dateDirPath)
                request.session['resultId'] = result.resultId
                return JsonResponse({
                    'user' : id,
                    'link' : video.link,
                    'id' : video.videoId,
                    'startTime' : video.startTime,
                    'duration' : video.duration,
                    'tag' : video.tag,
                    'dateDirPath': dateDirPath,
                })
            else:
                continue
    def post(self, request, id, emotionTag):
        return HttpResponseRedirect(reverse('realTimeResult'))

@api_view(['POST'])
def realTimeAnalyze(request):
    img = Image.open(request.FILES['image'])
    # Set image path and eeg path.
    imgName = request.data['image'].name
    eegName = 'test_signal.txt'
    #imgPath = os.path.join(request.data['dateDirPath'], 'face', imgName)
    global dateDirPath
    imgPath = os.path.join(os.path.join(dateDirPath, 'face'), imgName)
    eegTempPath = os.path.join(dirPath, eegName)
    # Save image to corresponding dir path.
    img.save(imgPath, "JPEG")

    emotionTag = request.data['videoTag']
    if(emotionTag =="happy"):
        emotionTag="happiness"
    elif(emotionTag =="sad"):
        emotionTag="sadness"
    highestEmotion, multiResult, faceResult, eegResult, sensorStatus = detectEmotion(imgPath, eegTempPath, emotionTag)
    # Accumulate results.
    global resultsDic
    emotions = ["happiness", "sadness", "disgust", "fear", "neutral"]
    for emotion in emotions:
        if emotion not in resultsDic:
            resultsDic[emotion] = [0, 0, 0]
        resultsDic[emotion][0] += faceResult[emotion]
        resultsDic[emotion][1] += eegResult[emotion]
        resultsDic[emotion][2] += multiResult[emotion]

    payload = {
        'emotionTag': highestEmotion,
        'emotionValues': multiResult,
        'faceValues': faceResult,
        'eegValues': eegResult,
        'eegConnections' : {
            "eeg1": int(sensorStatus[0]),
            "eeg2" : int(sensorStatus[1]),
            "eeg3" : int(sensorStatus[2]),
            "eeg4" : int(sensorStatus[3]),
            "eeg5" : int(sensorStatus[4]),
            "eeg6" : int(sensorStatus[5]),
            "eeg7" : int(sensorStatus[6]),
            "eeg8" : int(sensorStatus[7]),
        }
    }
    return JsonResponse(payload)

@api_view(['GET'])
def finalResult(request):
    # Create text to send signal to save accumulated EEG signal text.
    file = open(os.path.join(dirPath, "save.txt"), "w")
    file.write("Save accumulated EEG signals")
    file.close()
    # Save final result to DB.
    global resultsDic
    resultId = request.session.get('resultId')
    result = Result.objects.filter(pk=resultId).first()
    result.happiness = resultsDic['happiness'][2]
    result.sadness = resultsDic['sadness'][2]
    result.disgust = resultsDic['disgust'][2]
    result.fear = resultsDic['fear'][2]
    result.neutral = resultsDic['neutral'][2]
    result.save()
    payload = {
         "faceResult" : {
            'happiness' : resultsDic['happiness'][0],
            'sadness' : resultsDic['sadness'][0],
            'disgust' : resultsDic['disgust'][0],
            'fear' : resultsDic['fear'][0],
            'neutral' : resultsDic['neutral'][0],
        },
        "eegResult" : {
            'happiness' : resultsDic['happiness'][1],
            'sadness' : resultsDic['sadness'][1],
            'disgust' : resultsDic['disgust'][1],
            'fear' : resultsDic['fear'][1],
            'neutral' : resultsDic['neutral'][1],
        },
        "multiResult" : {
            'happiness' : resultsDic['happiness'][2],
            'sadness' : resultsDic['sadness'][2],
            'disgust' : resultsDic['disgust'][2],
            'fear' : resultsDic['fear'][2],
            'neutral' : resultsDic['neutral'][2],
        }
    }
    resultsDic = {}
    # Save accumulated EEG signal.
    filePath = os.path.join(dirPath, "all_signal.txt")
    destination = os.path.join(dateDirPath, "eeg")
    while True:
        if os.path.isfile(filePath):
            dest = shutil.move(filePath, destination)
            break
    return JsonResponse(payload)