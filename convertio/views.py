from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .convertor import Convertor
from django.views.generic import View
from django.http import HttpResponse
from subprocess import Popen
from .serializers import getConvertFormatsSerializer
import json


class getTokenView(APIView):

    def get(self, request):
        return Response({"msg": "not allowed method"})

    def post(self, request):
        c = Convertor()
        token = c.getToken()
        return Response({"token": token})


class getConvertFormats(APIView):
    serializer_class = getConvertFormatsSerializer

    def get(self, request):
        return Response({"msg": "not allowed method"})

    def post(self, request):
        ser = getConvertFormatsSerializer(data=request.data)
        if ser.is_valid():
            with open("static/formats.json", "r") as file:
                formats = json.loads(file.read())
                format = str(ser.data['ext']).upper()
                if format in formats:
                    return Response({"formats": formats[format]})
                else:
                    return Response({'res': "format not support"})
        else:
            return Response({"res": "fields not validate"})


class TestPage(View):
    def get(self, request):
        Popen("py test.py")
        return HttpResponse("keldi")
