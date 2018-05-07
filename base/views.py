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


@csrf_exempt
def general_search(request):
    users = User.objects.all()
    _request = request.POST['request']

    response = dict()

    for user in users:
        if _request in user.last_name or _request in user.first_name:
            response[user.get_full_name()] = {'url': user.get_absolute_url(),
                                              'avatar': user.settings.avatar}

    return JsonResponse({'response': response})
