from django.urls import path, include
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'post'

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    # path('', include('post.urls'))
]
