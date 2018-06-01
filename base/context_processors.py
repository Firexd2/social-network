def get_list_of_unread_rooms(user):
    rooms = user.settings.rooms.all()
    unread_rooms = []
    for room in rooms:
        if user not in room.messages.last().read.all():
            unread_rooms.append(room.id)

    return unread_rooms


def get_number_of_new_friends(user):
    return user.settings.subscribers.count()


def information(request):
    if request.user.is_authenticated:
        user = request.user
        user.save()

        user = request.user

        return {'unread_rooms': get_list_of_unread_rooms(user),
                'new_friends': get_number_of_new_friends(user)}
    return {}
