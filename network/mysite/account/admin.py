from django.contrib import admin

# Register your models here.
from .models import Profile


@admin.register(Profile)
class ProfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'image')