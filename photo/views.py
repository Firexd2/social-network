from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from base.views import GetUserMixin
from photo.models import PhotoAlbum, Photo
from django.views.generic.edit import FormMixin
from .forms import NewPhotoForm, NewAlbumForm
from django.http import HttpResponseRedirect


class ListAlbumView(GetUserMixin, FormMixin, ListView):
    model = PhotoAlbum
    template_name = 'albums.html'
    form_class = NewAlbumForm

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            album = form.save(commit=False)
            album.save()
            my_settings = self.request.user.settings
            my_settings.photo_albums.add(album)

        return redirect(self.request.get_full_path())

    def get_queryset(self):
        return PhotoAlbum.objects.filter(set_user__user=self.get_user)

    def get_context_data(self, **kwargs):
        context = super(ListAlbumView, self).get_context_data(**kwargs)
        return context


class DetailAlbumView(GetUserMixin, FormMixin, DetailView):
    model = PhotoAlbum
    template_name = 'album.html'

    def args_for_action(self):
        album = self.get_object()
        return album,

    def get_form(self, form_class=None):
        pass

    def action_cover(self, album):
        album.cover = self.request.POST['cover']
        album.save()
        return redirect(self.request.get_full_path())

    def action_description(self, album):
        album.name = self.request.POST['name']
        album.description = self.request.POST['description']
        album.save()
        return redirect(self.request.get_full_path())

    def action_photo(self, album):
        photo = Photo(photo=self.request.FILES['photo'])
        photo.save()
        album.photos.add(photo)
        return redirect(self.request.get_full_path())

    def action_delete(self, album):
        album.delete()
        return redirect(self.request.get_full_path())
