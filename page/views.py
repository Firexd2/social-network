from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import TemplateView, RedirectView

from base.mixins import UserMixin, MultiFormMixin
from page.forms import NewAvatarForm, NewWrittingWalForm, EditStatusForm
from photo.models import Photo, PhotoAlbum


class RedirectToMyPageView(LoginRequiredMixin, RedirectView):

    permanent = True
    pattern_name = 'page'

    def get_redirect_url(self, *args, **kwargs):
        user = self.request.user
        id = user.url_page if user.url_page else user.id_page
        return reverse(self.pattern_name, kwargs={'id': id})


class PageView(UserMixin, MultiFormMixin, TemplateView):
    template_name = 'page/index.html'

    form_classes = {'new_avatar': NewAvatarForm,
                    'new_writting_wall': NewWrittingWalForm,
                    'status': EditStatusForm}

    def get_instance_form_status(self):
        return self.request.user.settings

    def valid_form_new_avatar(self, form):

        photo = form.save()

        user = self.request.user
        user_settings = user.settings

        album, create = PhotoAlbum.objects.filter(set_user__user=user).\
            get_or_create(name='Фото со страницы')

        if create:
            user_settings.photo_albums.add(album)

        album.photos.add(photo)

        user_settings.avatar = photo.photo
        user_settings.save()

        return self.redirect_to_success_url()

    def valid_form_new_writting_wall(self, form):
        user = self.request.user
        current_user = self.get_user

        writting = form.save(commit=False)
        writting.author = user
        writting.save()

        current_user.settings.wall.add(writting)

        return self.redirect_to_success_url()

    def get_context_data(self, *args, **kwargs):
        context = super(PageView, self).get_context_data(**kwargs)
        context['last_photos'] = self.get_last_photos
        context['friends'] = self.get_user.settings.friends.all()
        context['online_friends'] = list(filter(lambda x: x.get_last_online == 'online', context['friends']))
        return context

    @property
    def get_last_photos(self):
        return Photo.objects.filter(album__set_user__user=self.get_user).order_by('-datetime')
