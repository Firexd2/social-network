from django.db import models
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill

from photo.models import PhotoAlbum


class SettingsUser(models.Model):

    subscriptions = models.ManyToManyField('user.User', related_name='subscriptions', blank=True)
    subscribers = models.ManyToManyField('user.User', related_name='subscribes', blank=True)
    friends = models.ManyToManyField('user.User', related_name='friends', blank=True)

    wall = models.ManyToManyField('WritingWall', blank=True)

    avatar = models.ImageField(max_length=200, default='no-image.gif/', null=True, blank=True)
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(40, 40)],
                                      format='JPEG',
                                      options={'quality': 100})

    avatar_50x50 = ImageSpecField(source='avatar',
                                  processors=[ResizeToFill(50, 50)],
                                  format='JPEG',
                                  options={'quality': 100})

    avatar_25x25 = ImageSpecField(source='avatar',
                                  processors=[ResizeToFill(25, 25)],
                                  format='JPEG',
                                  options={'quality': 100})

    status = models.CharField(max_length=100, blank=True, null=True)

    photo_albums = models.ManyToManyField(PhotoAlbum, blank=True, related_name='set_user')

    rooms = models.ManyToManyField('chat.Room', related_name='settings_user')


class WritingWall(models.Model):
    message = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey('user.User', on_delete=models.CASCADE, blank=True)
