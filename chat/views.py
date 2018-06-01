from django.shortcuts import render, redirect, reverse
from django.views.generic import ListView, DetailView, TemplateView, View
from base.mixins import UserMixin, ActionMixin, MultiFormMixin
from chat.models import Room, Message
from user.models import User
from django.db.models import Q, F

from django.shortcuts import Http404

from chat.forms import NewRoomForm, EditRoomLogoForm, EditRoomNameForm, OutRoomForm

from django.contrib.auth.mixins import LoginRequiredMixin

import tornadoredis

import json


def get_data(i, room):

    if room.type == 'conversation':

        name = room.name
        logo = room.logo
        info = str(room.settings_user.count()) + ' участника'

    else:
        other_user = [settings.user for settings in room.settings_user.all() if settings.user != i][0]

        name = other_user.get_full_name()
        logo = other_user.settings.avatar
        info = other_user.get_last_online

    return {'name': name, 'logo': logo, 'info': info, 'object': room}


class RoomsListView(LoginRequiredMixin, ActionMixin, ListView):

    template_name = 'chat/base.html'

    def get_queryset(self):

        user = self.request.user
        rooms = self.request.user.settings.rooms.all()
        data = []

        for room in rooms:
            data.append(get_data(user, room))

        return sorted(data, key=lambda i: i['object'].messages.last().datetime, reverse=True)


class SendMessageView(LoginRequiredMixin, ActionMixin, View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

    @staticmethod
    def get_dialog(addressee, destination):

        room = Room.objects.filter(Q(settings_user__user=addressee) and
                                   Q(settings_user__user=destination),
                                   type='dialog')
        return room[0]

    def send_alert_websocket(self, room, message):

        # отправляем оповещения о новом сообщении всем участникам комнаты, кроме самого себя

        notify = dict()

        for user in User.objects.filter(settings__rooms=room):
            if user != self.request.user:
                notify[user.id] = {'addressee': self.request.user.get_full_name(),
                                   'id_user': self.request.user.id,
                                   'type': room.type,
                                   'room_id': room.id,
                                   'avatar_25x25': self.request.user.settings.avatar_25x25.url,
                                   'avatar_40x40': self.request.user.settings.avatar_thumbnail.url,
                                   'time': str(message.datetime.strftime('%H:%M')),
                                   'text': message.text}

        self.client.publish('alert', json.dumps(notify))

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

                addressee.settings.rooms.add(room)
                destination.settings.rooms.add(room)

        # добавляем новое сообщение

        text = self.request.POST['action-new-message']

        message = Message(text=text, author=addressee)
        message.save()
        message.read.add(addressee)
        room.messages.add(message)

        # отправляем оповещения о новом сообщении

        self.send_alert_websocket(room, message)

        return redirect('/rooms/')


class RoomDetailView(LoginRequiredMixin, MultiFormMixin, DetailView):
    template_name = 'chat/chat.html'
    model = Room

    form_classes = {'edit_logo': EditRoomLogoForm,
                    'edit_name': EditRoomNameForm,
                    'out_room': OutRoomForm}

    form_success_urls = {'out_room': '/rooms/'}

    def valid_form_out_room(self, **kwargs):
        form = kwargs['form']

        room_id = form.cleaned_data['id']
        room = Room.objects.get(id=room_id)

        self.request.user.settings.rooms.remove(room)

        return super().redirect_to_success_url(**kwargs)

    def get_instance_form_edit_name(self, **kwargs):
        return self.get_object()['object']

    def get_instance_form_edit_logo(self, **kwargs):
        return self.get_object()['object']

    def get_object(self, queryset=None):
        room = get_data(self.request.user, super(RoomDetailView, self).get_object())
        self.read_to_message(room['object'])
        return room

    def read_to_message(self, room):

        user = self.request.user
        no_read_messages = room.messages.exclude(read=user)

        for message in no_read_messages:
            message.read.add(user)

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.settings.rooms.filter(id=kwargs['pk']):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)


class NewRoomView(LoginRequiredMixin, MultiFormMixin, TemplateView):
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

        # добавляем приветственное сообщение в беседу
        room.messages.add(message)

        return self.redirect_to_success_url(**kwargs)