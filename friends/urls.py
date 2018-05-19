
from django.urls import path
from friends import views as friends_views

urlpatterns = [
    path('', friends_views.FriendsListView.as_view(template_name='all_friends.html',
                                                   field='friends',
                                                   title='Все друзья'),
         name='friends'),

    path('subscribers/', friends_views.FriendsListView.as_view(template_name='subscribers.html',
                                                               field='subscribers',
                                                               title='Подписчики'),
         name='subscribers'),

    path('subscriptions/', friends_views.FriendsListView.as_view(template_name='subscriptions.html',
                                                                 field='subscriptions',
                                                                 title='Подписки'),
         name='subscriptions'),
]
