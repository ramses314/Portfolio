
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import path

from . import views
from .views import admin_load_excel, test_smtp_check, TestSMTPView
from ..events.viewsets import AdminEventChangeViewSet

app_name = 'main'

urlpatterns = [
    path(
        '',
        views.IndexView.as_view(),
        name='index',
    ),
    path(
        'api/v1/get-csrf-token/',
        views.get_csrf_token,
        name='get_csrf_token',
    ),
    path(
        'test/',
        staff_member_required(views.test),
        name='test-ws'
    ),
    path(
        'admin-custom/excel/',
        admin_load_excel,
        name='excel'
    ),
    path(
        'test_smtp/',
        test_smtp_check,
        name='smtp'
    ),
    path('api/v1/test_smtp/',
         TestSMTPView.as_view(),
         name='smtp-view'
    ),
    path(
        'admin-change/ticket/',
        AdminEventChangeViewSet.as_view(),
        name='admin-event-change'
    ),
]
