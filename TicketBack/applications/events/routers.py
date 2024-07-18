from rest_framework import routers

from . import viewsets

router = routers.DefaultRouter()

router.register(
    r'category',
    viewsets.CategoryViewSet,
    basename='category',
)

router.register(
    r'event',
    viewsets.EventViewSet,
    basename='event',
)

router.register(
    r'winners',
    viewsets.EventWinnersViewSet,
    basename='winners',
)

router.register(
    r'agr/home',
    viewsets.AgrHomeViewSet,
    basename='agr_home',
)

router.register(
    r'ticket',
    viewsets.TicketViewSet,
    basename='ticket',
)

router.register(
    r'prize',
    viewsets.PrizeViewSet,
    basename='prize',
)
