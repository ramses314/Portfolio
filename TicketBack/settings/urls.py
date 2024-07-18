from allauth.account.views import ConfirmEmailView
from dj_rest_auth.registration.views import VerifyEmailView, RegisterView
from dj_rest_auth.serializers import LoginSerializer
from dj_rest_auth.views import LoginView, PasswordResetConfirmView
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView, SpectacularSwaggerView
from rest_framework import routers

from applications.events.routers import router as events_router

from applications.sales.routers import router as sales_router

# DJANGO REST URLS
router = routers.DefaultRouter()

router.registry.extend(events_router.registry)
router.registry.extend(sales_router.registry)

urlpatterns_rest = [
    path('api/v1/', include(router.urls)),
]

# DJANGO SPECTACULAR URLS
urlpatterns_spectacular = [
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='schema',
    ),
    path(
        'api/schema/swagger',
        SpectacularSwaggerView.as_view(url_name='schema'),
        name='swagger',
    ),
    path(
        'api/schema/redoc/',
        SpectacularRedocView.as_view(url_name='schema'),
        name='redoc',
    ),
]

# DJANGO APPLICATIONS URLS
urlpatterns_applications = [
    path(
        '',
        include(('applications.main.urls', 'main'), namespace='main'),
    ),
    path(
        'api/v1/',
        include(('applications.login.urls', 'login'), namespace='login'),
    ),
    path(
        'api/v1/users/',
        include(('applications.users.urls', 'users'), namespace='users'),
    ),

]

# dj_rest_auth URLs
urlpatterns_auth = [
    path(
        'api/v1/auth/registrations/account-confirm-email/<str:key>/',
        ConfirmEmailView.as_view(),
        name='account_confirm_email'
    ),
    path('auth/email-verification-sent/',
         VerifyEmailView.as_view(),
         name='account_email_verification_sent'
         ),
    path(
        'api/v1/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
]


# AMAZON HEALTH
urlpatterns_amazon = [
    path(
        'health_check/',
        include(('health_check.urls', 'health_check'), namespace='health_check'),
    ),
]

# DJANGO URLS
urlpatterns = urlpatterns_spectacular + [
    path(
        'admin/',
        admin.site.urls,
    ),
] + urlpatterns_applications + urlpatterns_rest + urlpatterns_auth + urlpatterns_amazon

urlpatterns += staticfiles_urlpatterns() + \
    static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
