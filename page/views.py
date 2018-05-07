from django.urls import reverse
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, DetailView, RedirectView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin, TemplateResponseMixin
from base.views import GetUserMixin
from user.models import User
from photo.models import Photo, PhotoAlbum


class RedirectToMyPageView(LoginRequiredMixin, RedirectView):

    permanent = True
    pattern_name = 'page'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        id = user.url_page if user.url_page else user.id_page
        return reverse(self.pattern_name, kwargs={'id': id})


class PageView(GetUserMixin, View):
    model = User
    template_name = 'page.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data())

    def post(self, *args, **kwargs):
        user = self.get_user

        if self.request.FILES.get('photo'):
            user_settings = user.settings

            album, create = PhotoAlbum.objects.filter(set_user__user=user).get_or_create(name='Аватары')
            if create:
                user_settings.photo_albums.add(album)

            photo = Photo(photo=self.request.FILES['photo'])
            photo.save()

            album.photos.add(photo)

            user_settings.avatar = photo.photo
            user_settings.save()

        return redirect(self.request.get_full_path())

    def get_context_data(self):
        context = dict()
        context['object'] = self.get_user
        context['last_photos'] = self.get_last_photos
        return context

    @property
    def get_last_photos(self):
        return Photo.objects.filter(album__set_user__user=self.get_user).order_by('-datetime')[:4]


