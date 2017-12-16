from rest_framework import serializers
from .models import WebHook
from django import forms


class WebHookSerializer(serializers.ModelSerializer):
    class Meta:
        model = WebHook
        fields = ['event', 'oaid', 'fromuid', 'appid', 'msgid', 'message', 'timestamp', 'mac']


class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=100)
    file = forms.FileField()
