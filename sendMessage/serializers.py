from rest_framework import serializers


class sendMessage(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    msg = serializers.IntegerField()
    keyboard = serializers.JSONField(default="null")
    users = serializers.JSONField()
    type = serializers.IntegerField(default=1)
    keyboard_type = serializers.CharField(max_length=100, default="inline_keyboard")
    chat = serializers.IntegerField()
    parse = serializers.CharField(default="html", max_length=20)
