from django.urls import path
from .views import SignUpView, login_view, logout_view

app_name = 'account'

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='singup'),
    path('login/', login_view, name='login'),
    path('loginout/', logout_view, name='logout'),
]