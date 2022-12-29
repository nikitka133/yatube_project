from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post, User


def index(request):
    post_list = Post.objects.all()
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "page_obj": page_obj,
    }
    return render(request, "posts/index.html", context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    user = get_object_or_404(Group, slug=slug)
    post_list = Post.objects.filter(group__slug=slug)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {
        "post_username": user,
        "page_obj": page_obj,
        "group": group,
    }
    return render(request, "posts/group_list.html", context)


def profile(request, username):
    user = get_object_or_404(User.objects.filter(username=username))
    post_list = Post.objects.filter(author__username=username)
    paginator = Paginator(post_list, 10)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    count = Post.objects.filter(author__username=username).count()
    context = {"post_username": user, "page_obj": page_obj, "count": count}
    return render(request, "posts/profile.html", context)


def post_detail(request, post_id):
    page_obj = get_object_or_404(Post.objects.filter(pk=post_id))
    count = Post.objects.filter(author__username=page_obj.author.username).count()
    context = {"page_obj": page_obj, "count_posts": count}
    return render(request, "posts/post_detail.html", context)


def post_create(request):
    if request.method == "POST":
        author = Post(author=request.user)
        form = PostForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect(f"/profile/{request.user.username}/")
        else:
            context = {"form": form}
            return render(request, "posts/create.html", context)
    else:
        form = PostForm()
        print(form.fields)
        context = {"form": form}
        return render(request, "posts/create.html", context)


def post_edit(request, post_id):
    post = get_object_or_404(Post.objects.filter(pk=post_id))
    if request.method == "POST":
        author = Post(author=request.user)
        form = PostForm(request.POST, instance=author)
        if form.is_valid():
            form.save()
            return redirect(f"/posts/{post_id}/")
        else:
            context = {"form": form}
            return render(request, "posts/create.html", context)
    elif post.author.pk != request.user.id:
        return redirect(f"/posts/{post_id}/")
    else:
        form = PostForm(instance=post)
        context = {"form": form, "is_edit": True}
        return render(request, "posts/create.html", context)
