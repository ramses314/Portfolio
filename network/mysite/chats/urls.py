
from django.urls import path, include

from chats.views import plakat

app_name = 'chats'

urlpatterns = [
    path('', plakat, name='plakat')
]