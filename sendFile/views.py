from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import sendFileSerializer
from functions.file import File
from functions.run import Run
from api.models import tgBotModel


class sendFileView(APIView):
    serializer_class = sendFileSerializer

    def post(self, request):

        ser = sendFileSerializer(data=request.data)

        if not ser.is_valid():
            return Response({"msg": "Not Validate"})

        chat_id = ser.data.get("chat_id")
        url = ser.data.get("url")
        caption = ser.data.get("caption")
        fileType = ser.data.get("fileType")
        callback_url = ser.data.get("callback_url")
        token = tgBotModel.objects.filter(token=ser.data.get("token"))

        if token.count() == 0:
            return Response({"msg": "token Invalid"})
        token = token.first().botToken

        data = {
            "chat_id": chat_id,
            "url": url,
            "caption": caption,
            "fileType": fileType,
            "token": token,
            "callback_url": callback_url,
        }

        File.write("media/sendFile/data.json", data)

        Run.start("python ./sendFile/send.py")

        return Response({"msg": "keldi"})
