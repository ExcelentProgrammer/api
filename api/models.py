from django.db import models
from django.contrib.auth.models import User


class tgBotModel(models.Model):
    botToken = models.CharField(max_length=255)
    token = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.author.username
