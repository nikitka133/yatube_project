from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import PasswordChangeForm, UserCreationForm

User = get_user_model()


class CreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ChangePasswordForm(PasswordChangeForm):
    new_password1 = forms.CharField(
        label="Новый пароль",
        widget=forms.TextInput(attrs={"type": "password"}),
    )
    new_password2 = forms.CharField(
        label="Повтрите новый пароль",
        widget=forms.TextInput(attrs={"type": "password"}),
    )
