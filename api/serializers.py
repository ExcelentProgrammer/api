from djoser.serializers import UserCreateSerializer
from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(UserCreateSerializer):
    class Meta:
        model = User
        fields = ["first_name", "username", "email", "password"]


class sendMessageSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
