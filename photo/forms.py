from django import forms
from .models import PhotoAlbum, Photo


class NewAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['name', 'description']


class NewPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = []
