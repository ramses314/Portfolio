

from django.urls import path, include

from .views import users_search

app_name = 'search'

urlpatterns = [

    path('user_search/', users_search, name='user_search'),

]