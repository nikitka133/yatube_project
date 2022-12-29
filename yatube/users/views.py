from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .forms import ChangePasswordForm, CreationForm


class SignUp(CreateView):
    form_class = CreationForm
    success_url = reverse_lazy("posts:home")
    template_name = "users/signup.html"


class ChangePasswordView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    template_name = "users/change_password.html"
    success_message = "Пароль изменён"
    success_url = reverse_lazy("home")
    form_class = ChangePasswordForm
