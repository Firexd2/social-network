from datetime import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse

from page.models import SettingsUser
from user.manager import UserManager


def validate_url_page_on_unique(value):

    prohibited_names = ['settings', 'rooms', 'admin', 'auth',
                        'general_search', 'room', 'new-room',
                        'send_message', 'websocket']

    if value in prohibited_names:
        raise ValidationError(u'Адрес "%s" запрещён для использования' % value)


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True,
                              help_text='После регистрации на указанный e-mail будет выслано письмо активации')

    first_name = models.CharField('Имя', max_length=15)
    last_name = models.CharField('Фамилия', max_length=15)
    sex = models.CharField('Пол', max_length=1, choices=(('М', 'Мужской'), ('Ж', 'Женский')))
    marital_status = models.CharField('Семейное положение', max_length=20, blank=True, null=True)
    date_of_birth = models.DateField('Дата рождения', null=True, blank=True)
    city = models.CharField('Город', max_length=30, null=True, blank=True)
    employment = models.CharField('Тип деятельности', max_length=30, null=True, blank=True)

    url_page = models.SlugField('Адрес страницы', max_length=100,
                                validators=[validate_url_page_on_unique],
                                unique=True,
                                null=True,
                                blank=True)

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
        return self.url_page if self.url_page else self.id_page

    def get_albums_page_url(self):
        return reverse('albums', kwargs={'id': self.get_id})

    def get_friends_page_url(self):
        return reverse('friends', kwargs={'id': self.get_id})

    def get_subscribers_page_url(self):
        return reverse('subscribers', kwargs={'id': self.get_id})

    def get_subscriptions_page_url(self):
        return reverse('subscriptions', kwargs={'id': self.get_id})

    def get_absolute_url(self):
        return reverse('page', kwargs={'id': self.get_id})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    def get_string_last_activity(self, last, now):

        sex_suffix = 'а' if self.sex == 'Ж' else ''
        result = 'Заходил' + sex_suffix

        if last.date() == now.date():
            return result + ' сегодня в %s' % last.strftime('%H:%M')
        elif (now.date() - last.date()).days == 1:
            return result + ' вчера в %s' % last.strftime('%H:%M')
        else:
            return result + ' %s в %s' % (last.date(), last.strftime('%H:%M'))

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

        super().save(*args, **kwargs)

        if not self.id_page:
            self.id_page = 'id' + str(self.id)
            self.save()
