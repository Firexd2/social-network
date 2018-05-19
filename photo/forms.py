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
        fields = '__all__'
        widgets = {'photo': forms.FileInput(attrs={'class': 'form-control'})}


class CoverAlbumForm(forms.ModelForm):
    class Meta:
        model = PhotoAlbum
        fields = ['cover']


class DeleteAlbumForm(forms.ModelForm):

    id = forms.CharField(widget=forms.HiddenInput(attrs={'value': 'true'}))

    class Meta:
        model = PhotoAlbum
        fields = ['id']
