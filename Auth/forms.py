from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Ваш профиль не активирован. Пожалуйста, проверьте вашу почту!')
