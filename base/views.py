from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from user.models import User
from django.http import JsonResponse


class GetUserMixin(LoginRequiredMixin):

    @property
    def get_user(self):
        try:
            user = User.objects.get(url_page=self.kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=self.kwargs['id'])
        return user

    def post(self, *args, **kwargs):
        names = self.request.POST
        for name in names:
            handler_action = getattr(self, 'action_' + name.replace('-', '_'), None)
            if handler_action:
                return handler_action(*self.args_for_action())

    def get_context_data(self, *args, **kwargs):
        try:
            context = super().get_context_data(**kwargs)
        except AttributeError:
            context = dict()
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
                                              'avatar': user.settings.avatar}

    return JsonResponse({'response': response})
