
from django.urls import path, include
from posts.views import *


app_name = 'posts'
urlpatterns = [
    path('create/', create_post, name='create_post'),
]