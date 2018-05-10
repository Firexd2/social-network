from django.shortcuts import render
from base.views import GetUserMixin
from django.views.generic import View


class FriendsListView(GetUserMixin, View):
    template_name = 'friend_list.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data())

    @property
    def get_friends_list(self):
        return self.get_user.friends.all()

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_list'] = self.get_friends_list
        return context


class FriendRequestsView(GetUserMixin, View):
    template_name = 'friend_requests.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data())

    @property
    def get_friend_request_list(self):
        subscribes = []
        for subscribe in self.get_user.subscribes.all():
            if subscribe not in self.get_user.friends.all():
                subscribes.append(subscribe)
        return subscribes

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['friend_requests'] = self.get_friend_request_list
        return context
