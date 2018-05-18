from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView, View
from base.views import BaseView
from photo.models import PhotoAlbum, Photo
from django.views.generic.edit import FormMixin, DeletionMixin, DeleteView
from django.views.generic.detail import BaseDetailView
from django.http import HttpResponseRedirect

from base.mixins import MultiFormMixin, UserMixin
from .forms import AlbumForm, NewPhotoForm, CoverAlbumForm, DeleteAlbumForm


class ListAlbumView(BaseView, FormMixin, ListView):
    model = PhotoAlbum
    template_name = 'albums.html'
    form_class = AlbumForm

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


class DetailAlbumView(DetailView, UserMixin, MultiFormMixin):
    model = PhotoAlbum
    template_name = 'album.html'

    form_classes = {'new_photo': NewPhotoForm,
                    'album': AlbumForm,
                    'cover': CoverAlbumForm,
                    'delete': DeleteAlbumForm}

    def valid_form_new_photo(self, **kwargs):
        form = kwargs['form']
        photo = form.save(commit=False)
        photo.save()
        album = self.get_object()
        album.photos.add(photo)
        return super().redirect_to_success_url(**kwargs)

    def valid_form_delete(self, **kwargs):
        album = self.get_object()
        album.delete()
        return super().redirect_to_success_url(**kwargs)

    def get_success_url_form_delete(self):
        return self.request.user.get_albums_page_url()

    def get_instance_form_album(self):
        return self.get_object()

    def get_instance_form_cover(self):
        return self.get_object()

