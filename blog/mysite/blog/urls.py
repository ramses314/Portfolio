from django.urls import path
from .views import *

app_name = 'blog'

urlpatterns = [
    path('about_youtube/', tab_for_youtube, name='youtube'),
    path('search/', search, name='search'),
    path('', home, name='home'),
    path('<tag>/', collect_tag, name='collect_tag'),
    path('detail/<slug:slug>/', detail, name='detail'),

]

