from django.contrib.auth import views as auth_views
from django.urls import path

from user import views
from user.tools import activate

urlpatterns = [
    path('', views.LoginFormView.as_view()),
    path('registration/', views.RegisterFormView.as_view()),
    path('logout/', auth_views.logout_then_login),
    path(r'activate/<str:uidb64>/<str:token>/', activate, name='activate'),
]
