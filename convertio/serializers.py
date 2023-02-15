from rest_framework import serializers


class getConvertFormatsSerializer(serializers.Serializer):
    ext = serializers.CharField(max_length=30)
