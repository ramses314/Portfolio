from django.contrib import admin

# Register your models here.

from .models import *

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tags', 'created', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'post', 'body', 'created')
    list_filter = ('post', 'name', 'created')
    search_fields = ('name', 'body')

@admin.register(Blogger)
class BloggerAdmin(admin.ModelAdmin):
    list_display = ('title', 'text', 'image')
    list_filter = ('title', 'text', 'image')
    search_fields = ('title', 'text')