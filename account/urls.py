from django.urls import path
from .views import (SignUpView, login_view, logout_view, send_friend_request, accept_friend_request,
                    profile, notifications, show_profile, mark_asread, get_friends, send_message,
                    chat, conversation_history, search_friend)

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='singup'),
    path('login/', login_view, name='login'),
    path('loginout/', logout_view, name='logout'),
    path('send_friend_request/<str:to_username>', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<str:request_id>', accept_friend_request, name='accept_friend_request'),
    path('profile/<int:user_id>/', profile, name='profile'),
    path('show_profile/<int:user_id>/', show_profile, name='show_profile'),
    path('notification/', notifications, name='notification'),
    path('mark_asread/', mark_asread, name='mark_asread'),
    path('get_friends/', get_friends, name='get_friends'),
    path('chat_all/', chat, name='chat_all'),
    path('chat/<int:friend_id>/', chat, name='chat'),
    path('send_message/<int:friend_id>/', send_message, name='send_message'),
    path('conversation_history/<int:friend_id>/', conversation_history, name='conversation_history'),
    path('search/', search_friend, name='search_friend'),
]