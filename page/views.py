from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
from django.views.generic import TemplateView, DetailView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, TemplateResponseMixin
from base.views import BaseView
from user.models import User
from photo.models import Photo, PhotoAlbum
from .models import WritingWall


class RedirectToMyPageView(LoginRequiredMixin, RedirectView):

    permanent = True
    pattern_name = 'page'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        id = user.url_page if user.url_page else user.id_page
        return reverse(self.pattern_name, kwargs={'id': id})


class PageView(BaseView):
    template_name = 'page.html'

    def args_for_action(self):
        user = self.get_user
        return user,

    def action_avatar(self, *args):
        user = self.request.user
        user_settings = user.settings

        album, create = PhotoAlbum.objects.filter(set_user__user=user).\
            get_or_create(name='Фото со страницы')
        if create:
            user_settings.photo_albums.add(album)

        photo = Photo(photo=self.request.FILES['avatar'])
        photo.save()

        album.photos.add(photo)

        user_settings.avatar = photo.photo
        user_settings.save()

        return redirect(self.request.get_full_path())

    def action_wall(self, page_user):
        user = self.request.user

        writting_wall = WritingWall(message=self.request.POST['wall'], author=user)
        writting_wall.save()

        page_user.settings.wall.add(writting_wall)

        return redirect(self.request.get_full_path())

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_photos'] = self.get_last_photos
        context['friends'] = self.get_user.settings.friends.all()
        context['online_friends'] = list(filter(lambda x: x.get_last_online == 'online', context['friends']))
        return context

    @property
    def get_last_photos(self):
        return Photo.objects.filter(album__set_user__user=self.get_user).order_by('-datetime')


