from django.urls import path
from .views import SignUpView, login_view, logout_view, send_friend_request, accept_friend_request

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='singup'),
    path('login/', login_view, name='login'),
    path('loginout/', logout_view, name='logout'),
    path('send_friend_request/<str:to_username>', send_friend_request, name='send_friend_request'),
    path('accept_friend_request/<str:request_id>', accept_friend_request, name='accept_friend_request'),
]