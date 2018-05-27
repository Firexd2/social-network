from django.db import models
from django.urls import reverse
from photo.models import directory_path_photo


class Message(models.Model):
    author = models.ForeignKey('user.User', on_delete=models.CASCADE)
    text = models.TextField()
    datetime = models.DateTimeField(auto_now_add=True)
    read = models.ManyToManyField('user.User', related_name='having_read_user')


class Room(models.Model):
    name = models.CharField('Название беседы', max_length=20, null=True)
    logo = models.ImageField('Фотография беседы', upload_to=directory_path_photo, default='no-image.gif/')

    messages = models.ManyToManyField(Message)

    users = models.ManyToManyField('user.User')

    # def get_other_user(self, user):
    #     users = self.users.all()
    #     return [x for x in users if x != user][0]

    def get_absolute_url(self):
        return reverse('room', kwargs={'pk': self.id})

    @staticmethod
    def get_or_none(id_room):
        if id_room:
            try:
                return Room.objects.get(id=id_room)
            except Room.DoesNotExist:
                pass


# class Dialog(models.Model):
#     users = models.ManyToManyField('user.User')
#     messages = models.ManyToManyField(Message)


