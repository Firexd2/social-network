from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import ListView, DetailView
from base.views import GetUserMixin
from photo.models import PhotoAlbum, Photo
from django.views.generic.edit import FormMixin
from .forms import NewAlbumForm, NewPhotoForm
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt


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
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.get_user
        return context


class DetailAlbumView(GetUserMixin, FormMixin, DetailView):
    model = PhotoAlbum
    template_name = 'album.html'
    form_class = NewPhotoForm

    def post(self, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            photo = form.save(commit=False)
            photo.save()
            album = self.get_object()
            album.photos.add(photo)
        return redirect(self.request.get_full_path())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.get_user
        return context


@csrf_exempt
def edit_album(request, action):
    if request.POST:
        album = PhotoAlbum.objects.get(id=request.POST['id'])
        if action == 'cover':
            album.cover = request.POST['cover']
        elif action == 'description':
            album.name = request.POST['name']
            album.description = request.POST['description']

        if action == 'delete': album.delete()
        else: album.save()

        return HttpResponse('200')
