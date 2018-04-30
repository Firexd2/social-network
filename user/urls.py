from django.urls import path
from . import views
from .tools import activate
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.LoginFormView.as_view()),
    path('registration/', views.RegisterFormView.as_view()),
    path('logout/', auth_views.logout_then_login),
    path(r'activate/<uidb64>/<token>/', activate, name='activate'),
]
