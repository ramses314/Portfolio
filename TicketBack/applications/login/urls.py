from django.urls import path, include

from applications.login.serializers import CustomRegisterSerializer, LoginSerializer
from applications.login.views import CustomLoginView, CustomRegisterView, CustomVerifyEmail, CustomPasswordResetView

app_name = 'login'

urlpatterns = [
    path(
        'auth/registration/',
        CustomRegisterView.as_view(serializer_class=CustomRegisterSerializer),
        name='auth-register'
    ),
    path(
        'auth/login/',
        CustomLoginView.as_view(serializer_class=LoginSerializer),
        name='auth-login'
    ),
    path(
        'auth/password/reset/',
        CustomPasswordResetView.as_view(),
        name='rest_password_reset'
    ),
    path(
        'auth/',
        include('dj_rest_auth.urls'),
        name='auth-auth'
    ),
    path(
        'auth/registration/verify-email/',
        CustomVerifyEmail.as_view(),
        name='rest_verify_email'
    ),
    path(
        'auth/registration/',
        include('dj_rest_auth.registration.urls'),
        name='auth-registration'
    ),
]
