from chat.models import Message
from django import forms


# class NewMessageForm(forms.ModelForm):
#
#     class Meta:
#         model = Message
#         fields = ['text']
#         widgets = {'text': forms.Textarea(attrs={'class': 'form-control',
#                                                  'placeholder': 'Сообщение',
#                                                  'cols': '51',
#                                                  'rows': '5'})}
