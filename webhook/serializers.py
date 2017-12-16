from rest_framework import serializers
from .models import WebHook


class WebHookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebHook
        fields = ['event', 'oaid', 'fromuid', 'appid', 'msgid', 'message', 'timestamp', 'mac']
