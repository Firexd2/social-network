from django.shortcuts import redirect
from base.views import BaseView
from user.models import User


class FriendsListView(BaseView):

    template_name = field = title = ''

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['list'] = eval('self.get_user.settings.' + self.field + '.all()')
        context['title'] = self.title

        if self.request.GET.get('section') == 'online':
            context['list'] = list(filter(lambda x: x.get_last_online == 'online', context['list']))

        return context

    def args_for_action(self):
        return self.request.user, User.objects.get(id=self.request.POST['id'])

    def action_new_friend(self, user, other_user):

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

    def action_delete_friend(self, user, other_user):

        # checking for friends
        if user.settings.friends.filter(id=other_user.id):
            # remove friend
            user.settings.friends.remove(other_user)
            other_user.settings.friends.remove(user)
            # add subscriber and subscription
            user.settings.subscribers.add(other_user)
            other_user.settings.subscriptions.add(user)

        return redirect(self.request.get_full_path())





