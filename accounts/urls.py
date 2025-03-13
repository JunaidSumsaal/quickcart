from django.urls import path
from .views import (
    register_user, login_user, logout_user, profile,
    request_password_reset, reset_password, change_password
)

urlpatterns = [
    path("register/", register_user, name="register"),
    path("login/", login_user, name="login"),
    path("logout/", logout_user, name="logout"),
    path("profile/", profile, name="profile"),
    path("password-reset/", request_password_reset, name="password-reset"),
    path("reset-password/<uidb64>/<token>/", reset_password, name="reset-password"),
    path("change-password/", change_password, name="change-password"),
]
