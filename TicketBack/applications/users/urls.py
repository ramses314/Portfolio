from django.urls import path
from applications.users import views


urlpatterns = [
    path(
        'login/google/',
        views.GoogleUserInitApi.as_view(),
        name='login-google'
    ),
    path(
        'profile/',
        views.UserProfileView.as_view(),
        name='user-profile'
    ),
    path(
        'profile/add_hash/',
        views.UserAddHashView.as_view(),
        name='user-hash'
    ),
    path(
        'profile/delete_token/',
        views.UserDeletePaymentToken.as_view(),
        name='user-delete-token'
    ),
    path(
        'load_excel/',
        views.UserLoadExcel.as_view(),
        name='user-create-excel'
    ),
]
