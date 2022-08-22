from django.contrib import admin

from .models import Post


# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['body', 'slug', 'image', 'created']
    list_filter = ['created']
    search_fields = ['body']

