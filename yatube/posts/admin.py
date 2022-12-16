from django.contrib import admin

from .models import Post, Group


class PostAdmin(admin.ModelAdmin):
    list_display = 'pk', 'author', 'text', 'pub_date', 'group'
    search_fields = 'text',
    list_filter = 'pub_date',
    empty_value_display = '-пусто-'
    list_editable = ('group',)


class GroupAdmin(admin.ModelAdmin):
    list_display = 'title', 'slug', 'description'


admin.site.register(Post, PostAdmin)
admin.site.register(Group, GroupAdmin)