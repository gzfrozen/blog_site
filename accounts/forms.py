from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.models import User


class UserCreateForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"

    class Meta:
       model = User
       fields = ("username", "password1", "password2",)