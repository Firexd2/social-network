from django import forms
from .models import PhotoAlbum, Photo


class AlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['name', 'description']
        widgets = {'name': forms.TextInput(attrs={'class': 'form-control'}),
                   'description': forms.Textarea(attrs={'class': 'form-control'})
                   }


class NewPhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        exclude = []
        widgets = {'photo': forms.FileInput(attrs={'class': 'form-control'})}


class CoverAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['cover']


class DeleteAlbumForm(forms.ModelForm):

    id = forms.CharField(widget=forms.TextInput(attrs={'hidden': 'true', 'value': 'delete'}))

    class Meta:
        model = PhotoAlbum
        fields = ['id']
