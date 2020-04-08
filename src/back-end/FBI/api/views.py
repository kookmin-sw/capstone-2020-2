from django.http import HttpResponse, JsonResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import User
from . import serializers

@api_view(['GET','POST'])
def signup(request, format=None):
     if request.method == 'GET':
        user = User.objects.all()
        serializer = serializers.UserSerializer(user, many=True)
        return Response(serializer.data)

     if request.method == 'POST':
        serializer = serializers.UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     return HttpResponse("Bad request", status=400)

@api_view(['POST'])
def login(request, format=None):
    if request.method == 'POST':
        serializer = serializers.UserLoginSerializer(data=request.data)
        serializer.is_valid()

        if 'userFace' not in serializer.data:
            return HttpResponse("User's face image is required.", status=status.HTTP_204_NO_CONTENT)

        # TODO : Validation with userFace

        try:
            user = User.objects.get(userFace=serializer.data['userFace'])
        except User.DoesNotExist:
            return HttpResponse("Please sign up first", status=status.HTTP_409_CONFLICT)

        if user:
            payload = {
                'id': user.id,
                'username': user.username
            }
            return JsonResponse(payload)

