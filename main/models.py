from django.db import models
from webhook.models import WebHook


class Message(models.Model):
    class Meta:
        verbose_name = "Message"
        verbose_name_plural = "Messages"

    webhook = models.ForeignKey(WebHook, related_name='web_hook')
    respond = models.CharField(max_length=1000, blank=True)

    def __str__(self):
        return self.webhook.message
