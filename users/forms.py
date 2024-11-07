from mailings.forms import StyleMixin
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms
from users.models import User


class UserRegisterForm(StyleMixin, UserCreationForm):
    class Meta:
        model = User
        fields = (
            "email",
            "password1",
            "password2",
        )


class LoginCustomForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"


class PasswordRecoveryForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs["class"] = "form-control"

    class Meta:
        model = User
        fields = ("email",)
