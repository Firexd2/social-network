from django.views.generic import FormView
from django.contrib.auth import views as auth
from .forms import RegisterForm
from .forms import CustomAuthenticationForm
from .tools import send_verification_email, create_message
from django.http import HttpResponseRedirect
from base.views import BaseView


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


class SettingsPageView(BaseView):
    pass
