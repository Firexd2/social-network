from django.db import models
from django.urls import reverse

from sn import settings


def directory_path_photo(instance, filename):
    return 'photo/{0}/'.format(filename)


class PhotoAlbum(models.Model):
    name = models.CharField('Название альбома', max_length=20)
    description = models.TextField('Описание', blank=True, null=True)
    cover = models.CharField('Обложка', max_length=200, default=settings.NO_IMAGE)
    photos = models.ManyToManyField('Photo', related_name='album', blank=True)

    def get_absolute_url(self):
        user = self.set_user.first().user
        id = user.url_page if user.url_page else user.id_page
        return reverse('album', kwargs={'pk': self.id, 'id': id})

    def get_previous_url(self):
        user = self.set_user.first().user
        id = user.url_page if user.url_page else user.id_page
        return reverse('albums', kwargs={'id': id})


class Photo(models.Model):
    photo = models.ImageField('Фотография', upload_to=directory_path_photo)
    datetime = models.DateTimeField(auto_now_add=True)
