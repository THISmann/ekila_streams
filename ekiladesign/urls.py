from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import PubliciteViewSet


router = DefaultRouter()
router.register("", PubliciteViewSet, basename="publicities")

urlpatterns = [
    path("", include(router.urls)),
]
