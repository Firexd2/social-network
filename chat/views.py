from django.shortcuts import render
from django.views.generic import ListView
from base.mixins import UserMixin, ActionMixin
from chat.models import Thread
from user.models import User


class TheardsListView(ListView, UserMixin, ActionMixin):

    template_name = 'chat/base.html'
    action_renames = {'text': 'new_message'}

    def get_queryset(self):
        self.get_thread()
        return Thread.objects.filter(users=self.request.user)

    def get_thread(self, **kwargs):
        pass

    def action_new_message(self, **data):

        user = self.request.user
        other_user = self.get_user
