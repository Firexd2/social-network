from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm

from user.models import User


class EditSettingsForm(forms.ModelForm):

    class Meta:
        fields = ['first_name', 'last_name', 'sex', 'marital_status', 'date_of_birth', 'city', 'employment', 'url_page']
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'employment': forms.TextInput(attrs={'class': 'form-control'}),
            'url_page': forms.TextInput(attrs={'class': 'form-control'}),
            'marital_status': forms.TextInput(attrs={'class': 'form-control'}),
        }


class RegisterForm(UserCreationForm):

    password1 = forms.CharField(max_length=16, help_text='Ваш пароль не должен совпадать с вашим именем или'
                                                         ' другой персональной информацией или быть слишком похожим'
                                                         ' на неё. <br><br> Ваш пароль должен содержать как минимум'
                                                         ' 8 символов.<br><br> Ваш пароль не может быть одним из широко'
                                                         ' распространённых паролей.<br><br> Ваш пароль не может'
                                                         ' состоять только из цифр.',
                                widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    password2 = forms.CharField(max_length=16,
                                widget=forms.PasswordInput(attrs={'class': 'form-control',
                                                                  'placeholder': 'Повтор пароля'}))

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'sex', 'password1', 'password2']

        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'e-mail'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'}),
            'sex': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Пол'}),
        }


class CustomAuthenticationForm(AuthenticationForm):

    username = forms.CharField(widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Пароль'}))

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Ваш профиль не активирован. Пожалуйста, проверьте вашу почту!')
