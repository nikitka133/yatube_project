from django.shortcuts import render, get_object_or_404
from .models import Post, Group

LAST_POSTS = 10


def index(request):
    context = {'posts': Post.objects.all()[:LAST_POSTS]}
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    context = {
        'group': group,
        'posts': group.post.all()[:LAST_POSTS]
    }

    return render(request, 'posts/group_list.html', context)
