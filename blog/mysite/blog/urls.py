
from django.urls import path

from .views import *

app_name = 'blog'

urlpatterns = [
    path('search/', search, name='search'),
    path('', home, name='home'),
    path('<tag>/', home, name='home_with_tag'),
    path('detail/<slug:slug>/', detail, name='detail'),

]

