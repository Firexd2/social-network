from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView, TemplateView
from base.mixins import UserMixin, ActionMixin, MultiFormMixin
from chat.models import Room, Message
from user.models import User
from django.db.models import Q, F

from chat.forms import NewRoomForm

from django.contrib.auth.mixins import LoginRequiredMixin


def get_data(i, room):

    if room.users.count() > 2:

        name = room.name
        logo = room.logo
        info = str(room.users.count()) + ' участника'

    else:
        other_user = [user for user in room.users.all() if user != i][0]

        name = other_user.get_full_name()
        logo = other_user.settings.avatar
        info = other_user.get_last_online

    return {'name': name, 'logo': logo, 'info': info, 'object': room}


class RoomsListView(ListView, LoginRequiredMixin, ActionMixin):

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

                room = Room()
                room.save()
                room.users.add(addressee, destination)

                addressee.settings.rooms.add(room)
                destination.settings.rooms.add(room)

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
        room = get_data(self.request.user, super(RoomDetailView, self).get_object())
        self.read_to_message(room['object'])
        return room

    def read_to_message(self, room):

        user = self.request.user
        no_read_messages = room.messages.exclude(read=user)

        for message in no_read_messages:
            message.read.add(user)


class NewRoomView(TemplateView, LoginRequiredMixin, MultiFormMixin):
    template_name = 'chat/new_room.html'

    form_classes = {'new_room': NewRoomForm}

    def valid_form_new_room(self, **kwargs):

        # получаем форму, данные формы и экземляр user, создающего комнату
        form = kwargs['form']
        data = form.cleaned_data
        user = self.request.user

        # сохраняем форму и получаем экземпляр комнаты
        room = form.save()

        # создаем экземпляр сообщения
        message = Message(text=data['first_message'], author=user)
        message.save()

        # получаем экземпляры пользователей, которые будут в беседе
        users = [User.objects.get(id=user_id) for user_id in data['ids_users'].split(',')]
        users.append(user)

        # к каждому из пользователей добавляем созданную беседу
        for u in users:
            u.settings.rooms.add(room)

        # добавляем сообщение и участников в беседу
        room.users.add(*users)
        room.messages.add(message)

        return self.redirect_to_success_url(**kwargs)
