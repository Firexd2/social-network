from django.urls import path

from friends import views as friends_views

urlpatterns = [
    path('', friends_views.FriendsListView.as_view(template_name='friends/all_friends.html',
                                                   field='friends',
                                                   title='Все друзья'),
         name='friends'),

    path('subscribers/', friends_views.FriendsListView.as_view(template_name='friends/subscribers.html',
                                                               field='subscribers',
                                                               title='Подписчики'),
         name='subscribers'),

    path('subscriptions/', friends_views.FriendsListView.as_view(template_name='friends/subscriptions.html',
                                                                 field='subscriptions',
                                                                 title='Подписки'),
         name='subscriptions'),
]
