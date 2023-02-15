from django.shortcuts import render
from .models import tgBotModel
from rest_framework.response import Response
from rest_framework.views import APIView
from uuid import uuid4
from telebot import TeleBot
from .serializers import sendMessageSerializer
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.decorators import api_view


# from django.contrib.auth import authenticate, login


class tgBotView(APIView):
    serializer_class = sendMessageSerializer

    def post(self, request):
        ser = sendMessageSerializer(data=request.data)
        if not ser.is_valid():
            return Response({"msg": "Fields Not Validation"})
        botToken = ser.data.get("token")
        token = uuid4()

        try:
            bot = TeleBot(botToken)
            print(bot.get_me())
        except:
            return Response({"msg": "Bot Token Invalid"})

        check = tgBotModel.objects.filter(author=request.user, botToken=botToken).count()

        if check == 0:
            tgBotModel.objects.create(botToken=botToken, token=token, author=request.user)
        else:
            tgBotModel.objects.filter(author=request.user).update(botToken=botToken, token=token)

        return Response({"token": token})


@api_view(["GET"])
def test(request):
    return Response({"msg": "keldi"})
    # down = request.GET['down']
    # size = request.GET['size']
    # open("test.txt", "a").write(f"\n\n{down} - {size}")
