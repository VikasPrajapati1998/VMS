from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import VisitorViewSet, TurnstileViewSet, TurnstileLogViewSet

# Create a router and register viewsets
router = DefaultRouter()
router.register(r'visitors', VisitorViewSet, basename='visitor')
router.register(r'turnstiles', TurnstileViewSet, basename='turnstile')
router.register(r'turnstile-logs', TurnstileLogViewSet, basename='turnstilelog')

# URL patterns
urlpatterns = [
    path('', include(router.urls)),
]
