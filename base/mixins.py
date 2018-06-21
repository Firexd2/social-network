from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin

from user.models import User


class UserMixin(LoginRequiredMixin):

    @property
    def get_user(self):
        try:
            user = User.objects.get(url_page=self.kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=self.kwargs['id'])
        return user

    def get_context_data(self, *args, **kwargs):
        context = super(UserMixin, self).get_context_data(**kwargs)
        context['current_user'] = self.get_user
        return context


class ActionMixin(ContextMixin):

    def post(self, *args, **kwargs):

        dict_post = self.request.POST.copy()
        list_names = list(dict_post.keys())

        action_names = [name for name in list_names if 'action' == name[:6]]

        if len(action_names) != 1:
            raise AttributeError('You must have one action')

        name = action_names[0]

        action_handler = getattr(self, name.replace('-', '_'), None)

        return action_handler()
