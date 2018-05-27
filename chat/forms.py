from chat.models import Message, Room
from django import forms


class NewRoomForm(forms.ModelForm):

    ids_users = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'hidden': 'true'}))

    first_message = forms.CharField(label='Приветственное сообщение', required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '52', 'rows': '1'}))

    class Meta:
        model = Room
        fields = ['name', 'ids_users', 'first_message']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}


class EditRoomLogoForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['logo']
        widgets = {'logo': forms.FileInput(attrs={'class': 'form-control'})}


class EditRoomNameForm(forms.ModelForm):

    class Meta:
        model = Room
        fields = ['name']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'})}
