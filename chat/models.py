from django.db import models


class Message(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)


class Thread(models.Model):
    users = models.ManyToManyField('user.User')
    messages = models.ManyToManyField('Message')
