from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet
from .rider_views import DeliveryViewSet, DeliveryNotificationViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'deliveries', DeliveryViewSet, basename='delivery')
router.register(r'notifications', DeliveryNotificationViewSet, basename='notification')

urlpatterns = [
    path('', include(router.urls)),
]
