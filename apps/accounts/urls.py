"""URL path for user management on frontend."""

from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views import (
    ResetPasswordView,
    delete_user,
    password_change,
    user_login,
    user_logout,
    user_profile,
    user_register,
)

urlpatterns = [
    path("accounts/profile/", user_profile, name="profile"),
    path("delete-user/", delete_user, name="delete_user"),
    path("register/", user_register, name="register"),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
]
