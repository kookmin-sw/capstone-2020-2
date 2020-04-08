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




