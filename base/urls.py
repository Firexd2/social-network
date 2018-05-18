"""sn URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.page, name='page')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='page')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from page import views
from base.views import general_search
from sn import settings
from photo import views as photo_views
from friends import views as friends_views
from user import views as user_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('favicon.ico/', RedirectView.as_view(url='/static/image/favicon.ico'), name='favicon'),
    path('general_search/', general_search),
    path('', views.RedirectToMyPageView.as_view()),
    path('<str:id>/', views.PageView.as_view(), name='page'),
    path('<str:id>/albums/', photo_views.ListAlbumView.as_view(), name='albums'),
    path('<str:id>/album/<str:pk>/', photo_views.DetailAlbumView.as_view(), name='album'),
    path('<str:id>/friends/', include('friends.urls')),
    path('<str:id>/settings/', user_views.SettingsPageView.as_view(), name='settings'),

] + static(settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

