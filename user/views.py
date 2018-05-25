from django.contrib.auth import views as auth
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView, TemplateView

from base.mixins import MultiFormMixin, UserMixin
from user.forms import RegisterForm, CustomAuthenticationForm, EditSettingsForm
from user.tools import send_verification_email, create_message

from django.contrib.auth.mixins import LoginRequiredMixin


class LoginFormView(auth.LoginView):
    template_name = 'auth.html'
    redirect_authenticated_user = True
    form_class = CustomAuthenticationForm


class RegisterFormView(FormView):
    form_class = RegisterForm
    success_url = "/auth/"
    template_name = "registration.html"

    def form_valid(self, form):
        user = form.save(commit=False)
        email = user.email
        user.save()
        message = create_message(self.request, user)
        mail_subject = 'Активация аккаунта в социальной сети'
        send_verification_email(email, message, mail_subject)

        return HttpResponseRedirect('/')


class SettingsPageView(TemplateView, LoginRequiredMixin, MultiFormMixin):
    template_name = 'settings.html'

    form_classes = {'settings': EditSettingsForm}

    def get_instance_form_settings(self):
        return self.request.user

    def get_success_url_form_settings(self):
        return reverse('settings')
