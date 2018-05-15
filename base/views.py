from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.base import ContextMixin
from django.views.generic import View
from django.shortcuts import HttpResponse, render
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.http import JsonResponse


class BaseView(LoginRequiredMixin, ContextMixin, View):
    """
    Этот базовый класс помогает получать id пользователя,
    позволяет унаследоваться от ListView и DetailView,
    имеет диспетчер действий в пост запросах,
    держит в шаблоне текущего пользователя (current_user)
    """

    @property
    def get_user(self):
        try:
            user = User.objects.get(url_page=self.kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=self.kwargs['id'])
        return user

    def get(self, *args, **kwargs):
        try:
            super().get(self.request)
        except AttributeError:
            pass
        return render(self.request, self.template_name, self.get_context_data())

    def args_for_action(self):
        return []

    def post(self, *args, **kwargs):
        names = self.request.POST
        for name in names:
            handler_action = getattr(self, 'action_' + name.replace('-', '_'), None)
            if handler_action:
                return handler_action(*self.args_for_action())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.get_user
        return context


@csrf_exempt
def general_search(request):
    users = User.objects.all()
    request = request.POST['request']

    response = dict()

    for user in users:
        if request in user.last_name or request in user.first_name:
            response[user.get_full_name()] = {'url': user.get_absolute_url(),
                                              'avatar': user.settings.avatar_thumbnail.url}

    return JsonResponse({'response': response})
