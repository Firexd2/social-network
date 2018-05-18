from django.shortcuts import redirect
from base.mixins import ActionMixin, UserMixin
from django.views.generic import TemplateView
from user.models import User


class FriendsListView(TemplateView, UserMixin, ActionMixin):

    template_name = field = title = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = eval('self.get_user.settings.' + self.field + '.all()')
        context['title'] = self.title

        if self.request.GET.get('section') == 'online':
            context['list'] = list(filter(lambda x: x.get_last_online == 'online', context['list']))

        return context

    def action_add_friend(self):

        user = self.request.user
        other_user = User.objects.get(id=self.request.POST['add-friend'])

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

        user = self.request.user
        other_user = User.objects.get(id=self.request.POST['delete-friend'])

        # checking for friends
        if user.settings.friends.filter(id=other_user.id):
            # remove friend
            user.settings.friends.remove(other_user)
            other_user.settings.friends.remove(user)
            # add subscriber and subscription
            user.settings.subscribers.add(other_user)
            other_user.settings.subscriptions.add(user)

        return redirect(self.request.get_full_path())





