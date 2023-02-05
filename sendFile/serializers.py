from rest_framework import serializers


class sendFileSerializer(serializers.Serializer):
    url = serializers.URLField()
    chat_id = serializers.IntegerField()
    token = serializers.CharField(max_length=255)
    caption = serializers.CharField(default=None)
    fileType = serializers.CharField(max_length=100)
    callback_url = serializers.URLField()
