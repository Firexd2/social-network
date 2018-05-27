from django.shortcuts import redirect
from django.views.generic import TemplateView

from base.mixins import ActionMixin, UserMixin
from user.models import User


class FriendsListView(UserMixin, ActionMixin, TemplateView):

    template_name = field = title = ''

    def get_context_data(self, *args, **kwargs):
        context = super(FriendsListView, self).get_context_data(**kwargs)
        context['list'] = eval('self.get_user.settings.' + self.field + '.all()')
        context['title'] = self.title

        if self.request.GET.get('section') == 'online':
            context['list'] = list(filter(lambda x: x.get_last_online == 'online', context['list']))
        return context

    def action_add_friend(self):

        other_user_id = self.request.POST['action-add-friend']

        user = self.request.user
        other_user = User.objects.get(id=other_user_id)

        my_set = user.settings
        other_set = other_user.settings

        # checking for subscriptions
        if other_set.subscriptions.filter(id=user.id):

            my_set.friends.add(other_user)
            other_set.friends.add(user)

            other_set.subscriptions.remove(user)
            my_set.subscribers.remove(other_user)
        else:
            my_set.subscriptions.add(other_user)
            other_set.subscribers.add(user)

        return redirect(self.request.get_full_path())

    def action_delete_friend(self):

        other_user_id = self.request.POST['action-delete-friend']

        user = self.request.user
        other_user = User.objects.get(id=other_user_id)

        # checking for friends
        if user.settings.friends.filter(id=other_user_id):
            # remove friend
            user.settings.friends.remove(other_user)
            other_user.settings.friends.remove(user)
            # add subscriber and subscription
            user.settings.subscribers.add(other_user)
            other_user.settings.subscriptions.add(user)

        return redirect(self.request.get_full_path())
