import json

import tornadoredis
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import Http404
from django.shortcuts import HttpResponse
from django.views.generic import DetailView, ListView, TemplateView, View
from multi_form.mixin import MultiFormMixin

from base.mixins import ActionMixin
from chat.forms import EditRoomLogoForm, EditRoomNameForm, NewRoomForm, OutRoomForm
from chat.models import Message, Room
from user.models import User


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

    template_name = 'chat/rooms.html'

    def get_queryset(self):

        user = self.request.user
        rooms = self.request.user.settings.rooms.all()
        data = []

        for room in rooms:
            data.append(get_data(user, room))

        return sorted(data, key=lambda i: i['object'].messages.last().datetime, reverse=True)


class MessageView(LoginRequiredMixin, ActionMixin, View):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.client = tornadoredis.Client()
        self.client.connect()

    @staticmethod
    def get_dialog(addressee, destination):

        room = Room.objects. \
            filter(settings_user__user=addressee). \
            filter(settings_user__user=destination). \
            filter(type='dialog')

        if len(room) > 1:
            raise SystemError('В get_dialog room получился неоднозначным')

        return room[0] if room else None

    def action_reading_messages(self):

        user = self.request.user
        room = Room.objects.get(id=self.request.POST['room_id'])

        unread_messages = room.messages.exclude(read=user)

        for message in unread_messages:
            message.read.add(user)

        # создаем экземпляр вебсокет
        self.read_messages_to_websocket(room, user)

        return HttpResponse('200')

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

        # отправляем оповещение по вебсокету
        self.send_message_to_websocket(room, addressee, message)

        response = {'user_id': addressee.id,
                    'short_name': addressee.get_short_name(),
                    'time': message.get_time(),
                    'user_avatar_40x40': addressee.settings.avatar_thumbnail.url,
                    'text': message.text}

        return HttpResponse(json.dumps(response))

    def send_message_to_websocket(self, room, user, message):

        # отправляем оповещения о новом сообщении всем участникам комнаты, кроме самого себя

        notify = dict()

        if room.type == 'dialog':
            room_name = user.get_full_name()
            room_logo = user.settings.avatar_50x50.url
        else:
            room_name = room.name
            room_logo = room.logo_50x50.url

        for participant in User.objects.filter(settings__rooms=room):
            if participant != user:
                notify[participant.id] = {'user': user.get_full_name(),
                                          'user_id': user.id,
                                          'user_avatar_25x25': user.settings.avatar_25x25.url,
                                          'user_avatar_40x40': user.settings.avatar_thumbnail.url,
                                          'room_type': room.type,
                                          'room_id': room.id,
                                          'room_url': room.get_absolute_url(),
                                          'room_logo': room_logo,
                                          'room_name': room_name,
                                          'time': str(message.datetime.strftime('%H:%M')),
                                          'text': message.text,
                                          }

        self.client.publish('alert', json.dumps(notify))

    def read_messages_to_websocket(self, room, mine):

        # отправляем всем участникам диалога, что сообщения в беседе кем-то прочитаны

        users = User.objects.filter(settings__rooms=room)
        users_ids = ' '.join([str(user.id) for user in users if user != mine])

        self.client.publish('read', json.dumps({'rooms_id': str(room.id), 'users_ids': users_ids}))


class RoomDetailView(LoginRequiredMixin, MultiFormMixin, DetailView):
    template_name = 'chat/room.html'
    model = Room

    form_classes = {'edit_logo': EditRoomLogoForm,
                    'edit_name': EditRoomNameForm,
                    'out_room': OutRoomForm}

    form_success_urls = {'out_room': '/rooms/'}

    def form_valid_out_room(self, form):

        room_id = form.cleaned_data['id']
        room = Room.objects.get(id=room_id)

        self.request.user.settings.rooms.remove(room)

        return super().redirect_to_success_url()

    def get_instance_form_edit_name(self):
        return self.object['object']

    def get_instance_form_edit_logo(self):
        return self.object['object']

    def get_object(self, queryset=None):
        room = get_data(self.request.user, super(RoomDetailView, self).get_object())
        return room

    def dispatch(self, request, *args, **kwargs):

        if not self.request.user.settings.rooms.filter(id=kwargs['pk']):
            raise Http404()

        return super().dispatch(request, *args, **kwargs)


class NewRoomView(LoginRequiredMixin, MultiFormMixin, TemplateView):
    template_name = 'chat/new_room.html'

    form_classes = {'new_room': NewRoomForm}

    def form_valid_new_room(self, form):

        # получаем данные формы и экземляр user, создающего комнату
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
        # добавляем себя в список прочитавших это сообщение
        message.read.add(user)

        # создаем экземпляр вебсокет
        websocket = MessageView()
        # отправляем оповещение
        websocket.send_message_to_websocket(room, user, message)

        return self.redirect_to_success_url()
