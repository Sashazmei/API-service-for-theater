from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    GenreViewSet, ActorViewSet, PlayViewSet,
    TheatreHallViewSet, PerformanceViewSet,
    ReservationViewSet, TicketViewSet,
    BookTicketsView
)

router = DefaultRouter()
router.register(r'genres', GenreViewSet)
router.register(r'actors', ActorViewSet)
router.register(r'plays', PlayViewSet)
router.register(r'halls', TheatreHallViewSet)
router.register(r'performances', PerformanceViewSet)
router.register(r'reservations', ReservationViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('book/', BookTicketsView.as_view(), name='book-tickets'),
