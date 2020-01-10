from django.shortcuts import render
from django.views.generic.list import ListView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin

from django.contrib.auth.models import User
from blog.models import Post

# Create your views here.
class ProfileView(LoginRequiredMixin,ListView):
    model = Post
    template_name = 'accounts/profile.html'
    paginate_by = 1

    def get_queryset(self):
        username = self.kwargs['username']
        self.user = get_object_or_404(
            User, username=username)
        return super().get_queryset().filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username
        return context