from django.contrib import admin
from .models import *

from django import forms
from django.contrib import admin
from ckeditor.widgets import CKEditorWidget
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Post

# Register your models here.


class PostAdminForm(forms.ModelForm):
    body = forms.CharField(widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = '__all__'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'tags', 'created', 'status')
    list_filter = ('status', 'created', 'publish', 'author')
    search_fields = ('title', 'body')
    prepopulated_fields = {'slug' : ('title',)}
    raw_id_fields = ('author', )
    date_hierarchy = 'publish'
    ordering = ('status', 'publish')
    form = PostAdminForm


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



