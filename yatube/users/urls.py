from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import path

from . import views
from .views import SignUp

app_name = "users"

urlpatterns = [
    path(
        "logout/",
        LogoutView.as_view(template_name="users/logged_out.html"),
        name="logout",
    ),
    path("signup/", SignUp.as_view(), name="signup"),
    path("login/", LoginView.as_view(template_name="users/login.html"), name="login"),
    path(
        "reset/",
        PasswordResetView.as_view(template_name="users/password_reset.html"),
        name="password_reset_form",
    ),
    path(
        "accounts/settings/change_password",
        views.ChangePasswordView.as_view(),
        name="change_password",
    ),
]
