from django import forms

from page.models import WritingWall, SettingsUser
from photo.models import Photo


class NewAvatarForm(forms.ModelForm):

    class Meta:
        fields = '__all__'
        model = Photo
        widgets = {'photo': forms.FileInput(attrs={'class': 'form-control'})}


class NewWrittingWalForm(forms.ModelForm):

    class Meta:
        model = WritingWall
        fields = ['message']
        widgets = {'message': forms.Textarea(attrs={'class': 'form-control',
                                                    'placeholder': 'Что у вас нового?',
                                                    'cols': '51',
                                                    'rows': '2'})}


class EditStatusForm(forms.ModelForm):

    class Meta:
        model = SettingsUser
        fields = ['status']
        widgets = {'status': forms.TextInput(attrs={'class': 'form-control'})}
