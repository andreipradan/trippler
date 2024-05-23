from django import forms
from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UsernameField,
)
from django.core.exceptions import ValidationError

from authentication.models import User


class LoginForm(AuthenticationForm):
    username = UsernameField(
        widget=forms.EmailInput(
            attrs={"autofocus": True, "class": "form-control", "id": "floatingInput"},
        ),
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password"}),
    )


class RegisterForm(UserCreationForm):
    email = UsernameField(
        widget=forms.EmailInput(
            attrs={"autofocus": True, "class": "form-control", "id": "floatingInput"},
        ),
    )
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = User
        fields = ["email", "last_login"]

    def clean_password2(self) -> str:
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            msg = "Passwords don't match"
            raise ValidationError(msg)
        return password2

    def save(self, commit=True) -> "User":
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
