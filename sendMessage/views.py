from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import sendMessage as sendMessageSerializer
from functions import *
import os
from api.models import tgBotModel


class sendMessage(APIView):
    serializer_class = sendMessageSerializer

    def post(self, request):
        ser = sendMessageSerializer(data=request.data)

        if not ser.is_valid():
            return Response({"msg": "Not Validate"})

        msg = ser.data['msg']
        keyboard = ser.data['keyboard']
        users = ser.data['users']
        chat = ser.data['chat']
        type = ser.data['type']
        keyboard_type = ser.data['keyboard_type']
        parse = ser.data['parse']
        token = tgBotModel.objects.filter(token=ser.data.get("token"))

        if token.count() == 0:
            return Response({"msg": "token Invalid"})

        token = token.first().botToken

        File.write("media/sendMessage/data.json", {
            "token": token,
            "msg": msg,
            "keyboard": keyboard,
            "users": users,
            "chat": chat,
            "type": type,
            "keyboard_type": keyboard_type,
            "parse": parse,
        })

        Run.start("python ./sendMessage/task.py")

        res = {
            "msg": msg,
            "keyboard": keyboard,
            "users": len(users),
            "chat": chat,
            "type": type,
            "keyboard_type": keyboard_type,
            "parse": parse,
        }
        return Response(res)
