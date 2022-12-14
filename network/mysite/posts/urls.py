
from django.urls import path, include
from posts.views import *


app_name = 'posts'
urlpatterns = [
    path('create/', create_post, name='create_post'),
    path('post_detail/<id>/', post_detail, name='post_detail'),

    path('like/', post_like, name='post_like'),
    path('save_comments/', save_comment, name='save_comment')

]