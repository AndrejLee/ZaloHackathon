from __future__ import unicode_literals
from django.contrib import admin
from .models import Message


class MessageAdmin(admin.ModelAdmin):
    list_display = ('webhook', 'respond')
    search_fields = ['webhook', 'respond']
    list_per_page = 30

admin.site.register(Message, MessageAdmin)
