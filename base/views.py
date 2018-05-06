from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render

from user.models import User


class GetUserMixin(LoginRequiredMixin):

    @property
    def get_user(self):
        try:
            user = User.objects.get(url_page=self.kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=self.kwargs['id'])
        return user
