from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from base.mixins import UserMixin, ActionMixin
from chat.models import Room, Message
from user.models import User
from django.db.models import Q, F

from django.contrib.auth.mixins import LoginRequiredMixin



class TheardsListView(ListView, UserMixin, ActionMixin):

    template_name = 'chat/base.html'

    def get_queryset(self):

        user = self.request.user
        rooms = self.request.user.settings.rooms.all()

        queryset = []

        for room in rooms:
            if room.users.count() > 2:
                name = room.name
                logo = room.logo
            else:
                other_user = room.get_other_user(user.get_full_name())
                name = other_user.get_full_name()
                logo = other_user.settings.avatar

            queryset.append({'name': name, 'logo': logo, 'object': room})

        return queryset

    def get_dialog(self, addressee, destination):
        rooms = addressee.settings.rooms.filter(users=destination)
        for room in rooms:
            if room.users.count() == 2:
                return room

    def action_dialog_message(self):

        addressee = self.request.user
        destination = User.objects.get(id=self.request.POST['destination'])

        dialog = self.get_dialog(addressee, destination)

        if not dialog:
            dialog = Room()
            dialog.save()
            dialog.users.add(addressee, destination)

            addressee.settings.rooms.add(dialog)
            destination.settings.rooms.add(dialog)

        message = Message(text=self.request.POST['action-dialog-message'], author=addressee)
        message.save()
        dialog.messages.add(message)

        return redirect(self.request.get_full_path())


class ChatDetailView(DetailView, LoginRequiredMixin, ActionMixin):
    template_name = 'chat/chat.html'
    model = Room


