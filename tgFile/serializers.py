from rest_framework import serializers


class DownloadSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=255)
    chat_id = serializers.IntegerField()
    message_id = serializers.IntegerField()
    url = serializers.CharField()
