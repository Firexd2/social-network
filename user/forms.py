from django.contrib.auth.forms import UserCreationForm
from .models import User
from django.contrib.auth.forms import AuthenticationForm
from django import forms


class EditSettingsForm(forms.ModelForm):

    class Meta:
        fields = ['first_name', 'last_name', 'sex', 'date_of_birth', 'city', 'employment', 'url_page']
        model = User
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'sex': forms.Select(attrs={'class': 'form-control'}),
            'date_of_birth': forms.TextInput(attrs={'class': 'form-control'}),
            'city': forms.TextInput(attrs={'class': 'form-control'}),
            'employment': forms.TextInput(attrs={'class': 'form-control'}),
            'url_page': forms.TextInput(attrs={'class': 'form-control'}),
        }

    # def as_p(self):
    #     return self._html_output(
    #         normal_row='<p%(html_class_attr)s> %(field)s%(help_text)s</p>',
    #         error_row='%s',
    #         row_ender='</p>',
    #         help_text_html=' <span class="helptext">%s</span>',
    #         errors_on_separate_row=True,
    #     )


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'sex', 'last_name', 'password1', 'password2']


class CustomAuthenticationForm(AuthenticationForm):
    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Ваш профиль не активирован. Пожалуйста, проверьте вашу почту!')
