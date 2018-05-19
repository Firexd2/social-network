from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect, Http404
from django.views.generic.base import ContextMixin

from user.models import User


class UserMixin(LoginRequiredMixin):

    private_pages = ['settings', 'message']

    @property
    def get_user(self):
        try:
            user = User.objects.get(url_page=self.kwargs['id'])
        except User.DoesNotExist:
            user = User.objects.get(id_page=self.kwargs['id'])
        return user

    def dispatch(self, request, *args, **kwargs):

        current_page = request.path[1:-1].split('/')[-1]
        user_id = kwargs['id']

        if current_page in self.private_pages:
            if not (user_id == request.user.id_page or user_id == request.user.url_page):
                raise Http404()

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        context['current_user'] = self.get_user
        return context


class MultiFormMixin(ContextMixin):
    """
    form_classes => {'name_form': object_form}
    form_instances => {'name_form': instance} or def 'get_instance_form_' + name_form(self, **kwargs)
    form_initials => {'name_form': {'name_field': value}} or def 'get_initial_form_' + name_form(self, **kwargs)
    form_success_urls => {'name_form': success_url} or def 'get_success_urls_form_' + name_form(self, **kwargs)
    """

    form_classes = {}
    form_instances = {}
    form_initials = {}
    form_success_urls = {}

    def redirect_to_success_url(self, **kwargs):
        return HttpResponseRedirect(self.get_form_success_url(**kwargs))

    def get_form_initial(self, name_form):

        attr_name = 'get_initial_form_' + name_form
        default = self.form_initials.get(name_form)

        initial = getattr(self, attr_name, default)

        return initial() if callable(initial) else initial

    def get_form_instance(self, name_form):

        attr_name = 'get_instance_form_' + name_form
        default = self.form_instances.get(name_form)

        instance = getattr(self, attr_name, default)

        return instance() if callable(instance) else instance

    def get_form_success_url(self, **kwargs):
        name_form = kwargs['name_form']

        attr_name = 'get_success_url_form_' + name_form
        default = self.form_success_urls.get(name_form)

        success_url = getattr(self, attr_name, default)

        return success_url() if callable(success_url) else success_url or self.request.get_full_path()

    def general_valid_form(self, **kwargs):
        # general valid form
        form = kwargs['form']
        form.save()

        return self.redirect_to_success_url(**kwargs)

    def general_invalid_form(self, **kwargs):

        form = kwargs['form']
        name_form = kwargs['name_form']

        return self.render_to_response(self.get_context_data(**{'form_' + name_form: form}))

    def post(self, *args, **kwargs):

        data_names = set()
        data_names.update(set(self.request.POST.keys()))
        data_names.update(set(self.request.FILES.keys()))

        data_names.remove('csrfmiddlewaretoken')

        for name_form in self.form_classes:

            field_form_names = set(self.form_classes[name_form].base_fields.keys())

            if field_form_names == data_names:
                form = self.form_classes[name_form]
                form = form(self.request.POST, self.request.FILES, instance=self.get_form_instance(name_form))

                kwargs.update({'name_form': name_form, 'form': form})

                if form.is_valid():
                    handler = getattr(self, 'valid_form_' + name_form, self.general_valid_form)
                else:
                    handler = getattr(self, 'invalid_form_' + name_form, self.general_invalid_form)
                return handler(**kwargs)

    def get_form(self, name_form):
        form = self.form_classes[name_form]
        return form(initial=self.get_form_initial(name_form), instance=self.get_form_instance(name_form))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        for name_form in self.form_classes:
            if 'form_' + name_form not in kwargs:
                context['form_' + name_form] = self.get_form(name_form)
        return context


class ActionMixin:

    suffix_method = 'action_'

    def post(self, *args, **kwargs):
        dict_post = self.request.POST.copy()
        dict_post.pop('csrfmiddlewaretoken', None)

        name = list(dict_post.keys())

        if len(name) != 1:
            raise AttributeError

        handler_action = getattr(self, self.suffix_method + name[0].replace('-', '_'), None)
        return handler_action()
