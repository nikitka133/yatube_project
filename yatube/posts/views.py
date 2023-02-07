from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page

from .forms import CommentForm, PostForm
from .models import Follow, Group, Post, User


def get_page_obj(request, post_list):
    return Paginator(post_list, 10).get_page(request.GET.get("page"))


@cache_page(20, key_prefix="index_page")
def index(request):
    post_list = Post.objects.all().select_related("group")
    page_obj = get_page_obj(request, post_list)
    context = {"page_obj": page_obj, "index": True}
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.all()
    page_obj = get_page_obj(request, post_list)
    context = {
        "page_obj": page_obj,
        "group": group,
    }

    return render(request, "posts/group_list.html", context)


def profile(request, username):
    user = get_object_or_404(User.objects.filter(username=username))
    post_list = user.posts.all()
    page_obj = get_page_obj(request, post_list)

    context = {
        "author": user,
        "page_obj": page_obj,
    }

    if request.user.is_authenticated:
        following = request.user.follower.exists()
        context.update(following=following)

    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    page_obj = get_object_or_404(Post.objects.filter(pk=post_id))
    form = CommentForm()
    comments = page_obj.comments.all()
    context = {
        "form": form,
        "page_obj": page_obj,
        "comments": comments,
    }
    return render(request, "posts/post_detail.html", context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
        files=request.FILES or None,
    )
    context = {"form": form}
    if request.method == "GET" or not form.is_valid():
        return render(request, "posts/create.html", context)
    else:
        form.instance.author = request.user
        form.save()
        return redirect("posts:profile", request.user.username)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.filter(pk=post_id))
    form = PostForm(
        request.POST or None, files=request.FILES or None, instance=post
    )
    context = {
        "form": form,
        "page_obj": post,
    }
    if post.author.pk != request.user.id:
        return redirect("posts:post_detail", post_id)
    if form.is_valid():
        form.save()
        return redirect("posts:post_detail", post_id)

    context["is_edit"] = True
    return render(request, "posts/create.html", context)


@login_required
def add_comment(request, post_id):
    post = Post.objects.get(pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect("posts:post_detail", post_id=post_id)


@login_required
def follow_index(request):
    posts = Post.objects.filter(author__following__user=request.user)
    page_obj = get_page_obj(request, posts)
    context = {"page_obj": page_obj, "follow": True}
    return render(request, "posts/follow.html", context)


@login_required
def profile_follow(request, username):
    user = get_object_or_404(User, username=username)
    if request.user.username != username:
        Follow.objects.get_or_create(user=request.user, author=user)
    return redirect("posts:profile", username)


@login_required
def profile_unfollow(request, username):
    user = get_object_or_404(User, username=username)
    Follow.objects.filter(user=request.user, author=user).delete()
    return redirect("posts:profile", username)
