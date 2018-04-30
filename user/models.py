from __future__ import unicode_literals
from django.db import models
# from django.core.mail import send_mail
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import ugettext_lazy as _
from .manager import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email'), unique=True)
    url = models.CharField(_('url'), max_length=200, unique=True, blank=True, null=True)
    first_name = models.CharField(_('name'), max_length=30)
    last_name = models.CharField(_('surname'), max_length=30)
    date_joined = models.DateTimeField(_('registered'), auto_now_add=True)
    is_active = models.BooleanField(_('is_active'), default=True)
    is_staff = models.BooleanField(default=False)
    id_page = models.SlugField('id_page', max_length=100, blank=True)
    url_page = models.SlugField('url_page', max_length=100, unique=True, null=True, blank=True)
    settings = models.OneToOneField('SettingsUser', on_delete=models.CASCADE, blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')

    def get_absolute_url(self):
        from django.urls import reverse
        if self.url_page:
            return reverse('page', kwargs={'id': self.url_page})
        else:
            return reverse('page', kwargs={'id': self.id_page})

    def get_full_name(self):
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        return self.first_name

    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def save(self, *args, **kwargs):

        if not self.settings:
            settings = SettingsUser()
            settings.save()
            self.settings = settings

        super(User, self).save(*args, **kwargs)
        if not self.id_page:
            self.id_page = 'id' + str(self.id)
            self.save()


class SettingsUser(models.Model):

    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    date_of_birth = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    employment = models.CharField(max_length=30, null=True, blank=True)
