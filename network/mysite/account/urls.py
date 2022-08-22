from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from django.contrib import auth as aauth

from .views import *

app_name = 'account'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password_reset/confirm/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password_change/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('registration/', registration, name='registration'),


    path('', home, name='home'),
    path('edit/', edit, name='edit'),
    path('follower_list/', follower_list, name='follower_list'),
    path('subs_list/', subs_list, name='subs_list'),



]
