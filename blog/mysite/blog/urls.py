
from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns = [
    path('', home, name='home'),
    path('detail/<slug:slug>/', detail, name='detail')
]