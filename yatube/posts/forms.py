from django import forms

from .models import Post, Group


class PostForm(forms.ModelForm):
    text = forms.Textarea()
    group = forms.ModelChoiceField(queryset=Group.objects.all(), required=False)

    class Meta:
        model = Post
        fields = ('text', 'group')



# class PostForm(forms.Form):
#     text = forms.CharField(required=True)
#     group = forms.ChoiceField(required=False)
