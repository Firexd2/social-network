from django.urls import reverse
from django.views.generic import TemplateView, DetailView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin
from user.models import User


class RedirectToMyPageView(LoginRequiredMixin, RedirectView):

    permanent = True
    pattern_name = 'page'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.url_page:
            id = self.request.user.url_page
        else:
            id = self.request.user.id_page
        return reverse(self.pattern_name, kwargs={'id': id})


class PageView(TemplateView):
    model = User
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            user = User.objects.get(url_page=kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=kwargs['id'])
        context['object'] = user
        return context


