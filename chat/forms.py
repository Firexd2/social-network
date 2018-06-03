from chat.models import Message, Room
from django import forms


class NewRoomForm(forms.ModelForm):

    ids_users = forms.CharField(label='', required=False, widget=forms.TextInput(attrs={'hidden': 'true'}))

    first_message = forms.CharField(label='Приветственное сообщение', required=False,
                                    widget=forms.Textarea(attrs={'class': 'form-control', 'cols': '52', 'rows': '1'}))

    type = forms.CharField(label='', widget=forms.TextInput(attrs={'style': 'display:none', 'value': 'conversation'}))

    class Meta:
        model = Room
        fields = ['name', 'ids_users', 'first_message', 'type']
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


class OutRoomForm(forms.ModelForm):
    id = forms.IntegerField(label='', widget=forms.TextInput())

    class Meta:
        model = Room
        fields = ['id']


class SendMessageForm(forms.ModelForm):

    id = forms.CharField()
    destination = forms.CharField()

    class Meta:
        model = Message
        fields = ['text', 'id', 'destination']

