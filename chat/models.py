from datetime import datetime, timedelta

from django.db import models
from django.urls import reverse
from django.utils import dateformat
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from photo.models import directory_path_photo


class Message(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    read = models.ManyToManyField('user.User', related_name='having_read_user')

    def get_time(self):
        datetime_now = datetime.now()
        if datetime_now.date() == self.datetime.date():
            return dateformat.format(self.datetime, 'H:i')

        if datetime_now.date() - timedelta(days=1) == self.datetime.date():
            return 'Вчера ' + dateformat.format(self.datetime, 'H:i')

        if datetime_now.year == self.datetime.year:
            return dateformat.format(self.datetime, 'j E H:i')

        return self.datetime


class Room(models.Model):
    name = models.CharField('Название беседы', max_length=20, null=True)
    logo = models.ImageField('Фотография беседы', upload_to=directory_path_photo, default='no-image.gif/')

    logo_50x50 = ImageSpecField(source='logo',
                                processors=[ResizeToFill(50, 50)],
                                format='JPEG',
                                options={'quality': 100})

    # dialog or conversation
    type = models.CharField('Тип комнаты', max_length=12, default='dialog')

    messages = models.ManyToManyField(Message)

    def get_absolute_url(self):
        return reverse('room', kwargs={'pk': self.id})

    @staticmethod
    def get_or_none(id_room):
        if id_room:
            try:
                return Room.objects.get(id=id_room)
            except Room.DoesNotExist:
                pass
