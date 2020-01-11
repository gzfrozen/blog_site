from django.shortcuts import render, redirect
from django.views.generic import CreateView, ListView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.contrib.auth import login, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from blog.models import Post
from accounts.forms import UserCreateForm

# Create your views here.


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/profile.html'
    paginate_by = 1

    def get_queryset(self):
        username = self.kwargs['username']
        login_username = self.request.user.username
        if not login_username == username:
            raise Http404('Not authorized to view.')
        self.user = get_object_or_404(
            User, username=username)
        return super().get_queryset().filter(user=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username
        return context


class SignupFormView(CreateView):
    template_name = 'accounts/signup.html'

    def post(self, request, *args, **kwargs):
        form = UserCreateForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            group = Group.objects.get(name='norm_user')
            user.groups.add(group)
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            auth = authenticate(username=username, password=password)
            login(request, auth)
            return redirect('accounts:profile', self.request.POST.get('username'))
        return render(request, 'accounts/signup.html', {'form': form, })

    def get(self, request, *args, **kwargs):
        form = UserCreateForm(request.POST)
        return render(request, 'accounts/signup.html', {'form': form, })
