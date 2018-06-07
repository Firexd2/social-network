from django.contrib import admin

from chat.models import Message, Room

admin.site.register(Message)
admin.site.register(Room)
