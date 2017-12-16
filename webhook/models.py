from django.db import models


class WebHook(models.Model):
    class Meta:
        verbose_name = "WebHook"

    event = models.CharField(max_length=100)
    oaid = models.BigIntegerField(default=0)
    fromuid = models.BigIntegerField(default=0)
    appid = models.BigIntegerField(default=0, null=True)
    msgid = models.CharField(max_length=100)
    message = models.TextField()
    timestamp = models.BigIntegerField(default=0)
    mac = models.CharField(max_length=1000)

    def __str__(self):
        return '{}-{}'.format(self.message, self.timestamp)
