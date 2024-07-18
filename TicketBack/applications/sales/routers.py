from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()

router.register(
    r'order',
    viewsets.OrderViewSet,
    basename='order'
)

router.register(
    r'order/delete',
    viewsets.OrderDestroyViewSet,
    basename='order_destroy'
)
