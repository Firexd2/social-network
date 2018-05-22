from django.db import models
from django.urls import reverse
from photo.models import directory_path_photo


class Message(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)


class Room(models.Model):
    name = models.CharField(max_length=20, blank=True, null=True)
    logo = models.ImageField('Фотография', upload_to=directory_path_photo, blank=True, null=True)
    messages = models.ManyToManyField(Message)

    users = models.ManyToManyField('user.User')

    def get_other_user(self, user):
        users = self.users.all()
        return [x for x in users if x != user][0]

    def get_absolute_url(self):
        return reverse('chat', kwargs={'pk': self.id})


# class Dialog(models.Model):
#     users = models.ManyToManyField('user.User')
#     messages = models.ManyToManyField(Message)


