from django.urls import reverse
from django.views.generic import TemplateView, DetailView, RedirectView
from django.contrib.auth.mixins import LoginRequiredMixin

from base.views import GetUserMixin
from user.models import User


class RedirectToMyPageView(LoginRequiredMixin, RedirectView):

    permanent = True
    pattern_name = 'page'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        id = user.url_page if user.url_page else user.id_page
        return reverse(self.pattern_name, kwargs={'id': id})


class PageView(GetUserMixin, TemplateView):
    model = User
    template_name = 'page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['object'] = self.get_user
        return context


