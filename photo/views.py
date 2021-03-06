from django.shortcuts import redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormMixin
from multi_form.mixin import MultiFormMixin

from base.mixins import UserMixin
from photo.forms import AlbumForm, NewPhotoForm, CoverAlbumForm, DeleteAlbumForm
from photo.models import PhotoAlbum, Photo


class ListAlbumView(UserMixin, FormMixin, ListView):
    model = PhotoAlbum
    template_name = 'photo/albums.html'
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
        context = super().get_context_data(**kwargs)
        context['all_photos'] = Photo.objects.filter(album__set_user__user=self.get_user)
        return context


class DetailAlbumView(UserMixin, MultiFormMixin, DetailView):
    model = PhotoAlbum
    template_name = 'photo/album.html'

    form_classes = {'new_photo': NewPhotoForm,
                    'album': AlbumForm,
                    'cover': CoverAlbumForm,
                    'delete': DeleteAlbumForm}

    def form_valid_new_photo(self, form):
        photo = form.save(commit=False)
        photo.save()
        album = self.get_object()
        album.photos.add(photo)
        return super().redirect_to_success_url()

    def form_valid_delete(self, form):
        album = self.get_object()
        album.delete()
        return super().redirect_to_success_url()

    def get_success_url_form_delete(self):
        return self.request.user.get_albums_page_url()

    def get_instance_form_album(self):
        return self.get_object()

    def get_instance_form_cover(self):
        return self.get_object()
