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

from base.views import general_search
from page import views
from photo import views as photo_views
from sn import settings
from user import views as user_views
from chat import views as chat_views

urlpatterns = [
    path('', views.RedirectToMyPageView.as_view()),
    path('admin/', admin.site.urls),
    path('auth/', include('user.urls')),
    path('favicon.ico/', RedirectView.as_view(url='/static/image/favicon.ico'), name='favicon'),
    path('general_search/', general_search),
    path('room/<str:pk>/', chat_views.RoomDetailView.as_view(), name='room'),
    path('new-room/', chat_views.NewRoomView.as_view(), name='new-room'),
    path('rooms/', chat_views.RoomsListView.as_view(), name='rooms'),
    path('send_message/', chat_views.MessageView.as_view(), name='send-message'),
    path('settings/', user_views.SettingsPageView.as_view(), name='settings'),
    path('<str:id>/', views.PageView.as_view(), name='page'),
    path('<str:id>/albums/', photo_views.ListAlbumView.as_view(), name='albums'),
    path('<str:id>/album/<str:pk>/', photo_views.DetailAlbumView.as_view(), name='album'),
    path('<str:id>/friends/', include('friends.urls')),

] + static(settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

