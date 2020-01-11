from django.urls import path, include

from accounts.views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('profile/<str:username>',
         ProfileView.as_view(), name='profile'),
    path('signup',
         SignupFormView.as_view(), name='signup'),
]
