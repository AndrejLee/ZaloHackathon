from __future__ import unicode_literals
from django.contrib import admin
from .models import WebHook


class WebhookAdmin(admin.ModelAdmin):
    list_display = ('event', 'oaid', 'fromuid', 'appid', 'msgid', 'message', 'timestamp', 'mac')
    search_fields = ('event', 'oaid', 'fromuid', 'appid', 'msgid', 'message', 'timestamp', 'mac')
    list_per_page = 30

admin.site.register(WebHook, WebhookAdmin)
