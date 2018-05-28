from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from user.models import User


# class BaseView(LoginRequiredMixin, ContextMixin, View):
#     """
#     Этот базовый класс помогает получать id пользователя,
#     позволяет унаследоваться от ListView и DetailView,
#     имеет диспетчер действий в пост запросах,
#     дополнительно позволяет выводить нужные формы,
#     держит в шаблоне текущего пользователя (current_user)
#     """
#
#     forms = {}
#
#     @property
#     def get_user(self):
#         try:
#             user = User.objects.get(url_page=self.kwargs['id'])
#         except User.DoesNotExist:
#             user = User.objects.get(id_page=self.kwargs['id'])
#         return user
#
#     def get(self, *args, **kwargs):
#         try:
#             super().get(self.request)
#         except AttributeError:
#             pass
#         return render(self.request, self.template_name, self.get_context_data())
#
#     def args_for_action(self):
#         return []
#
#     def post(self, *args, **kwargs):
#         dict_post = self.request.POST
#         dict_post.pop('csrfmiddlewaretoken', None)
#
#         name = dict_post.keys()
#
#         if len(name) != 1:
#             raise AttributeError
#
#         handler_action = getattr(self, 'action_' + name[0].replace('-', '_'), None)
#         return handler_action
#
#     def get_context_data(self, *args, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['current_user'] = self.get_user
#         if self.forms:
#             for key in self.forms:
#                 context['form_' + key] = self.forms[key](initial=getattr(self, 'get_initial_' + key, None)(), instance=None)
#         return context


@csrf_exempt
def general_search(request):
    users = User.objects.all()
    request = request.POST['request'].lower()

    response = dict()

    for user in users:
        if request in user.last_name.lower() or request in user.first_name.lower():
            response[user.get_full_name()] = {'url': user.get_absolute_url(),
                                              'avatar': user.settings.avatar_thumbnail.url}

    return JsonResponse({'response': response})
