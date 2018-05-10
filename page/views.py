from django.urls import reverse
from django.shortcuts import render, redirect, HttpResponse
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
    template_name = 'page.html'

    def get(self, *args, **kwargs):
        return render(self.request, self.template_name, self.get_context_data())

    def args_for_action(self):
        user = self.get_user
        return user,

    def action_avatar(self, user):
        user_settings = user.settings

        album, create = PhotoAlbum.objects.filter(set_user__user=user).get_or_create(name='Фото со страницы')
        if create:
            user_settings.photo_albums.add(album)

        photo = Photo(photo=self.request.FILES['avatar'])
        photo.save()

        album.photos.add(photo)

        user_settings.avatar = photo.photo
        user_settings.save()

        return redirect(self.request.get_full_path())

    def action_new_friend(self, user):

        my_user = self.request.user
        other_user = User.objects.get(id=self.request.POST['new-friend'])

        my_user.settings.subscribers.add(other_user)

        if other_user.settings.subscribers.filter(id=my_user.id):
            print('YESSSSS')
            my_user.settings.friends.add(other_user)
            other_user.settings.friends.add(my_user)

        return HttpResponse('200')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_photos'] = self.get_last_photos
        return context

    @property
    def get_last_photos(self):
        return Photo.objects.filter(album__set_user__user=self.get_user).order_by('-datetime')[:4]


