from django import forms

from .models import Group, Post


class PostForm(forms.ModelForm):
    text = forms.Textarea()
    group = forms.ModelChoiceField(
        queryset=Group.objects.all(), required=False
    )

    class Meta:
        model = Post
        fields = ("text", "group")
