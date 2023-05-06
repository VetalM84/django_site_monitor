"""Forms management."""

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserChangeForm, UserCreationForm

from apps.accounts.models import User


class UserLoginForm(AuthenticationForm):
    """User login form on frontend."""

    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )


class UserRegisterForm(UserCreationForm):
    """User register form on frontend."""

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )
    password2 = forms.CharField(
        label="Repeat password",
        widget=forms.PasswordInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        required = False
        fields = ("email", "password1", "password2")


class UserProfileForm(forms.ModelForm):
    """User profile form on frontend."""

    first_name = forms.CharField(
        required=False,
        label="First name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    last_name = forms.CharField(
        required=False,
        label="Last name",
        widget=forms.TextInput(attrs={"class": "form-control"}),
    )
    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )

    class Meta:
        model = User
        exclude = ("password",)
        fields = ("first_name", "last_name", "email")


class CustomUserCreationForm(UserCreationForm):
    """Custom User creation form on backend."""

    class Meta:
        model = User
        fields = "__all__"


class CustomUserChangeForm(UserChangeForm):
    """Custom User changing form on backend."""

    class Meta:
        model = User
        fields = "__all__"
