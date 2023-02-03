from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import DownloadSerializer
from api.models import tgBotModel
from functions.run import Run
from re import match


class DownloadAPI(APIView):
    serializer_class = DownloadSerializer

    def post(self, request):
        ser = DownloadSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"msg": "Not Validate"})

        token = tgBotModel.objects.filter(token=ser.data.get("token"))

        if token.count() == 0:
            return Response({"msg": "token Invalid"})

        token = token.first().botToken
        chat_id = ser.data.get("chat_id")
        message_id = ser.data.get("message_id")
        url = ser.data.get("url")

        if not match(r"^(https|http)://(.*)$",url):
            return Response({"msg": "url Not Valid"})

        Run.start(f"python tgFile/down.py {token} {chat_id} {message_id} {url}")

        return Response({"msg": token})
