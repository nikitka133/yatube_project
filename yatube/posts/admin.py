from django.contrib import admin

from .models import Comment, Follow, Group, Post


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "author", "text", "pub_date", "group")
    search_fields = ("text",)
    list_filter = ("pub_date",)
    empty_value_display = "-пусто-"
    list_editable = ("group",)


class GroupAdmin(admin.ModelAdmin):
    list_display = ("title", "slug", "description")


class FollowAdmin(admin.ModelAdmin):
    list_display = ("author", "user")


class CommentAdmin(admin.ModelAdmin):
    list_display = ("post", "author", "text")


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Follow, FollowAdmin)
