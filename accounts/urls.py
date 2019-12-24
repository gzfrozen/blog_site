from django.urls import path, include
from django.contrib.auth import views as auth_views

app_name = 'accounts'
urlpatterns = [
    path('', include('django.contrib.auth.urls')),
]
