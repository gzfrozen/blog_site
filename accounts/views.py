from django.db import transaction
from django.views.generic import CreateView, ListView
from django.contrib.auth.views import LoginView
from django.shortcuts import get_object_or_404
from django.http import Http404
from django.urls import reverse_lazy
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import Group

from django.contrib.auth.models import User
from blog.models import Post
from accounts.forms import UserCreateForm

# Create your views here.


class CustomLoginView(LoginView):
    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['username'].widget.attrs["class"] = "form-control"
        form.fields['password'].widget.attrs["class"] = "form-control"
        return form


class SignupFormView(CreateView):
    template_name = 'accounts/signup.html'
    form_class = UserCreateForm

    def form_valid(self, form):
        with transaction.atomic():
            valid = super().form_valid(form)
            group = Group.objects.get(name='norm_user')
            self.object.groups.add(group)
        login(self.request, self.object)
        return valid

    def get_success_url(self):
        return reverse_lazy('accounts:profile', kwargs={'username': self.object.username})


class ProfileView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'accounts/profile.html'
    login_url = '/accounts/login'
    paginate_by = 5

    def get_queryset(self):
        username = self.kwargs['username']
        # login_username = self.request.user.username
        # if not login_username == username:
        #     raise Http404('Not authorized to view.')
        self.user = get_object_or_404(
            User, username=username)
        return super().get_queryset().filter(created_by=self.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['username'] = self.user.username
        return context
