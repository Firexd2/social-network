from __future__ import unicode_literals
from datetime import datetime
from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.urls import reverse
from .manager import UserManager
from page.models import SettingsUser


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)

    url = models.CharField(max_length=200, unique=True, blank=True, null=True)

    first_name = models.CharField('Имя', max_length=30)
    last_name = models.CharField('Фамилия', max_length=30)
    sex = models.CharField('Пол', max_length=1, choices=(('М', 'Мужской'), ('Ж', 'Женский')))
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город', max_length=30, null=True, blank=True)
    employment = models.CharField('Тип деятельности', max_length=30, null=True, blank=True)
    url_page = models.SlugField('Адрес страницы', max_length=100, unique=True, null=True, blank=True)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    id_page = models.SlugField(max_length=100, blank=True)
    settings = models.OneToOneField('page.SettingsUser', on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

    @property
    def get_id(self):
        id = self.url_page if self.url_page else self.id_page
        return id

    def get_albums_page_url(self):
        return reverse('albums', kwargs={'id': self.get_id})

    def get_friends_page_url(self):
        return reverse('friends', kwargs={'id': self.get_id})

    def get_subscribers_page_url(self):
        return reverse('subscribers', kwargs={'id': self.get_id})

    def get_subscriptions_page_url(self):
        return reverse('subscriptions', kwargs={'id': self.get_id})

    def get_settings_page_url(self):
        return reverse('settings', kwargs={'id': self.get_id})

    def get_absolute_url(self):
        return reverse('page', kwargs={'id': self.get_id})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    @staticmethod
    def get_string_last_activity(last, now):
        if last.date() == now.date():
            return 'Заходил сегодня в %s:%s' % (last.hour, last.minute)
        elif (now.date() - last.date()).days == 1:
            return 'Заходил вчера в %s:%s' % (last.hour, last.minute)
        else:
            return 'Заходил %s в %s:%s' % (last.date(), last.hour, last.minute)

    @property
    def get_last_online(self):

        now = datetime.now().replace(tzinfo=None)
        last = self.last_activity
        difference = (now - last).seconds
        if difference > 600:
            return self.get_string_last_activity(last, now)
        else:
            return 'online'

    def save(self, *args, **kwargs):

        if not self.settings:
            settings = SettingsUser()
            settings.save()
            self.settings = settings

        super(User, self).save(*args, **kwargs)

        if not self.id_page:
            self.id_page = 'id' + str(self.id)
            self.save()
