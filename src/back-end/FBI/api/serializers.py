from .models import User
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'userFace']

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['userFace']