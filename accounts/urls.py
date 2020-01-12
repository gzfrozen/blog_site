from django.urls import path, include

from accounts.views import *
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
    path('login', CustomLoginView.as_view(), name='login'),
    path('signup',
         SignupFormView.as_view(), name='signup'),
    path('profile/<str:username>',
         ProfileView.as_view(), name='profile'),
]
