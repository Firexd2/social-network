from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from base.mixins import UserMixin, ActionMixin
from chat.models import Room, Message
from user.models import User
from django.db.models import Q, F

from django.contrib.auth.mixins import LoginRequiredMixin


def get_data(user, room):

    if room.users.count() > 2:
        name = room.name
        logo = room.logo
        info = str(room.users.count()) + ' участн.'
    else:
        other_user = room.get_other_user(user)

        name = other_user.get_full_name()
        logo = other_user.settings.avatar
        info = other_user.get_last_online

    return {'name': name, 'logo': logo, 'info': info, 'object': room}


class RoomsListView(ListView, UserMixin, ActionMixin):

    template_name = 'chat/base.html'

    def get_queryset(self):

        user = self.request.user
        rooms = self.request.user.settings.rooms.all()
        data = []

        for room in rooms:
            data.append(get_data(user, room))

        return sorted(data, key=lambda i: i['object'].messages.last().datetime, reverse=True)

    @staticmethod
    def get_dialog(addressee, destination):
        rooms = addressee.settings.rooms.filter(users=destination)
        for room in rooms:
            if room.users.count() == 2:
                return room

    def action_new_message(self):

        addressee = self.request.user

        # пробуем получить комнату
        room = Room.get_or_none(self.request.POST.get('room-id'))

        if not room:

            # если комнату не получили, значит пользователь пишет с главной страницы
            # пробуем получить диалог по двум юзерам: по отправителю и адресату

            destination = User.objects.get(id=self.request.POST['destination'])

            room = self.get_dialog(addressee, destination)

            if not room:

                # такой комнаты нету, создаем её

                dialog = Room()
                dialog.save()
                dialog.users.add(addressee, destination)

                addressee.settings.rooms.add(dialog)
                destination.settings.rooms.add(dialog)

        # добавляем новое сообщение

        message = Message(text=self.request.POST['action-new-message'], author=addressee)
        message.save()
        message.read.add(addressee)
        room.messages.add(message)

        return redirect(self.request.get_full_path())


class RoomDetailView(DetailView, LoginRequiredMixin, ActionMixin):
    template_name = 'chat/chat.html'
    model = Room

    def get_object(self, queryset=None):
        room = get_data(self.request.user, super().get_object())
        self.read_to_message(room['object'])
        return room

    def read_to_message(self, room):

        user = self.request.user
        no_read_messages = room.messages.exclude(read=user)

        for message in no_read_messages:
            message.read.add(user)

